"""
YouTube Video Summarizer — Agentic RAG with FastAPI + SSE
Uses LangChain + Groq for summarization and RAG-based Q&A.
HuggingFace local embeddings + FAISS for vector storage.
Server-Sent Events for real-time streaming.
"""

import os
import re
import json
import time
import asyncio
from typing import Optional

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ─── Config ───────────────────────────────────────────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GEN_MODEL = "llama-3.3-70b-versatile"
EMBED_MODEL = "all-MiniLM-L6-v2"
FAISS_DIR = "extra-files/faiss_index"
AUDIO_DIR = "extra-files"

os.makedirs(AUDIO_DIR, exist_ok=True)

# ─── FastAPI App ──────────────────────────────────────────────────────────────
app = FastAPI(title="YouTube Video Summarizer — Agentic RAG")
templates = Jinja2Templates(directory="templates")

# ─── In-memory state per video ────────────────────────────────────────────────
video_store: dict = {}  # video_id -> { transcript, summary, chunks, metadata, faiss }

# ─── LangChain LLM & Embeddings ──────────────────────────────────────────────
llm = ChatGroq(model=GEN_MODEL, api_key=GROQ_API_KEY)
embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)


# ═══════════════════════════  HELPERS  ═══════════════════════════════════════

def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    raise ValueError("Invalid YouTube URL")


def get_video_metadata(url: str) -> dict:
    """Fetch video title, thumbnail, duration, channel using yt-dlp."""
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
        info = ydl.extract_info(url, download=False)
    return {
        "title": info.get("title", "Unknown"),
        "thumbnail": info.get("thumbnail", ""),
        "duration": info.get("duration", 0),
        "channel": info.get("channel", info.get("uploader", "Unknown")),
        "view_count": info.get("view_count", 0),
        "upload_date": info.get("upload_date", ""),
        "description": (info.get("description", "") or "")[:500],
    }


# ── Tier 1: YouTube Transcript API (instant, no download) ────────────────────

def get_youtube_transcript(video_id: str) -> tuple[str | None, str | None, list | None]:
    """Fetch YouTube's native subtitles via youtube-transcript-api.
    Returns (plain_text, timestamped_text, raw_segments) or (None, None, None)."""
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        transcript_obj = None
        # Prefer manually created transcripts
        try:
            transcript_obj = transcript_list.find_manually_created_transcript(["en", "hi", "en-US", "en-GB"])
        except Exception:
            pass

        # Fallback: auto-generated
        if not transcript_obj:
            try:
                transcript_obj = transcript_list.find_generated_transcript(["en", "hi", "en-US", "en-GB"])
            except Exception:
                pass

        # Last resort: any available transcript
        if not transcript_obj:
            try:
                for t in transcript_list:
                    transcript_obj = t
                    break
            except Exception:
                pass

        if not transcript_obj:
            return None, None, None

        fetched = transcript_obj.fetch()

        segments = []
        raw_segments = []
        timestamped_parts = []
        last_ts_mark = -30

        for s in fetched.snippets:
            if not s.text.strip():
                continue
            segments.append(s.text.strip())
            raw_segments.append({
                "text": s.text.strip(),
                "start": round(s.start, 2),
                "duration": round(s.duration, 2) if hasattr(s, 'duration') else 0,
            })
            start = s.start
            if start - last_ts_mark >= 30:
                mins = int(start) // 60
                secs = int(start) % 60
                timestamped_parts.append(f"\n\n[{mins:02d}:{secs:02d}]\n")
                last_ts_mark = start
            timestamped_parts.append(s.text.strip())

        plain = " ".join(segments).strip()
        timestamped = " ".join(timestamped_parts).strip()

        if len(plain) < 50:
            return None, None, None
        return plain, timestamped, raw_segments

    except Exception as e:
        print(f"[Transcript Error] {e}")
        return None, None, None


# ── Smart Transcription (YouTube Transcript API only) ─────────────────────────

def smart_transcribe(url: str, video_id: str, progress_callback=None) -> tuple[str, str, str, list]:
    """
    Fetch transcript via youtube-transcript-api — instant, free, no download.
    Returns: (transcript_text, timestamped_text, method_used, raw_segments)
    """
    if progress_callback:
        progress_callback("transcript_yt", "Fetching YouTube transcript...")
    transcript, timestamped, raw_segments = get_youtube_transcript(video_id)
    if transcript:
        return transcript, timestamped, "youtube_native", raw_segments or []

    raise RuntimeError("No transcript available for this video. The video may not have subtitles/captions enabled.")


def split_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[str]:
    """Split transcript into overlapping chunks using LangChain splitter."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap, length_function=len
    )
    return splitter.split_text(text)


def embed_and_store(video_id: str, chunks: list[str]) -> FAISS:
    """Embed chunks with LangChain Gemini embeddings and store in FAISS."""
    vectorstore = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=[{"video_id": video_id, "chunk_index": i} for i in range(len(chunks))],
    )
    return vectorstore


def retrieve_context(query: str, video_id: str, top_k: int = 5) -> list[str]:
    """Vector search in FAISS for relevant chunks."""
    store_data = video_store.get(video_id)
    if not store_data or "faiss" not in store_data:
        return []
    vectorstore: FAISS = store_data["faiss"]
    docs = vectorstore.similarity_search(query, k=top_k)
    return [doc.page_content for doc in docs]


# ═══════════════════════════  AGENTIC FUNCTIONS  ════════════════════════════

def generate_summary(transcript: str, chunks: list[str], style: str = "detailed") -> str:
    """Agentic Map-Reduce summary over chunks."""
    partials = []
    batch_size = 3
    for i in range(0, len(chunks), batch_size):
        batch = "\n\n".join(chunks[i : i + batch_size])
        prompt = (
            f"Summarize this transcript section. Style: {style}. "
            "Focus on key points, story flow, names, and concepts.\n\n"
            f"{batch}"
        )
        out = llm.invoke(prompt)
        partials.append(out.content)
        time.sleep(0.3)

    final_prompt = f"""Create one final {style} summary from these section summaries.
Output in Markdown with:
1. **Summary** — a paragraph overview  
2. **Key Takeaways** — 6-8 bullet points  
3. **Core Concepts** — table with Concept | Description  
4. **Conclusion** — 3-4 line wrap-up

{chr(10).join(partials)}"""

    final = llm.invoke(final_prompt)
    return final.content


def generate_chapters(transcript: str) -> str:
    """Generate chapter-like sections from the transcript."""
    prompt = f"""Analyze this transcript and create chapter-style sections.
For each chapter, provide:
- A short title
- Time estimate (approximate)
- 2-3 line summary

Output in clean Markdown format.

{transcript}"""
    resp = llm.invoke(prompt)
    return resp.content


def generate_key_concepts(transcript: str) -> str:
    """Extract key concepts, terms, people mentioned."""
    prompt = f"""Extract all key concepts, terms, people, and ideas from this transcript.
Output as a Markdown table with columns: Concept | Description | Significance
Include at least 8-10 items.

{transcript}"""
    resp = llm.invoke(prompt)
    return resp.content


def generate_mindmap(transcript: str) -> str:
    """Generate a text-based mind map of the video content."""
    prompt = f"""Create a structured mind map of this video's content.
Use indented bullet points to show hierarchy:
- Main Topic
  - Sub-topic 1
    - Detail A
    - Detail B
  - Sub-topic 2
    - Detail C

Make it comprehensive, covering all major themes and ideas discussed.

{transcript}"""
    resp = llm.invoke(prompt)
    return resp.content


def generate_notes(transcript: str) -> str:
    """Generate structured study notes from the transcript."""
    prompt = f"""Create comprehensive study notes from this video transcript.
Format in Markdown with:
1. **Title & Overview** — brief topic summary
2. **Key Points** — numbered list of main ideas
3. **Important Details** — supporting bullet points
4. **Definitions & Terms** — any concepts explained
5. **Examples Mentioned** — practical examples from the video
6. **Quick Revision** — 5-6 bullet points for quick review

Make notes concise, well-organized, and easy to study from.

{transcript}"""
    resp = llm.invoke(prompt)
    return resp.content


def rag_answer(query: str, video_id: str) -> str:
    """Agentic RAG: retrieve context + generate answer."""
    context_docs = retrieve_context(query, video_id, top_k=5)
    context_text = "\n\n---\n\n".join(context_docs)

    prompt = f"""You are an AI assistant for a YouTube video. Answer the question using ONLY the retrieved context below.
If the answer is not in the context, say so clearly.
Be detailed but concise. Use Markdown formatting.

**User Question:** {query}

**Retrieved Context:**
{context_text}"""

    response = llm.invoke(prompt)
    return response.content


# ═══════════════════════════  API MODELS  ═══════════════════════════════════

class ProcessRequest(BaseModel):
    url: str

class ChatRequest(BaseModel):
    video_id: str
    message: str

class FeatureRequest(BaseModel):
    video_id: str
    feature: str  # "summary", "chapters", "concepts", "mindmap"
    style: Optional[str] = "detailed"


# ═══════════════════════════  SSE HELPERS  ═══════════════════════════════════

def sse_event(event: str, data: dict) -> str:
    """Format an SSE event string."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


# ═══════════════════════════  ROUTES  ═══════════════════════════════════════

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/process")
async def process_video(req: ProcessRequest):
    """Process a YouTube video: download → transcribe → chunk → embed. Streams progress via SSE."""

    async def event_stream():
        try:
            # Step 1: Extract video ID & metadata
            video_id = extract_video_id(req.url)
            yield sse_event("progress", {"step": "metadata", "message": "Fetching video info..."})
            await asyncio.sleep(0)

            metadata = await asyncio.to_thread(get_video_metadata, req.url)
            yield sse_event("metadata", {"video_id": video_id, **metadata})

            # Clean up previous video data (fresh context for each video)
            if video_store:
                old_ids = [vid for vid in video_store if vid != video_id]
                for old_id in old_ids:
                    del video_store[old_id]

            # Check if already processed
            if video_id in video_store and video_store[video_id].get("transcript"):
                yield sse_event("progress", {"step": "cached", "message": "Video already processed — using cache"})
                yield sse_event("complete", {
                    "video_id": video_id,
                    "transcript": video_store[video_id]["transcript"],
                    "timestamped_transcript": video_store[video_id].get("timestamped_transcript", ""),
                    "summary": video_store[video_id].get("summary", ""),
                })
                return

            # Step 2: Smart Transcription (YouTube native → Gemini fallback)
            yield sse_event("progress", {"step": "transcript_yt", "message": "Trying YouTube native transcript (fastest)..."})
            await asyncio.sleep(0)

            # We use a container to pass progress from the sync callback
            progress_updates = []
            def progress_cb(step, msg):
                progress_updates.append((step, msg))

            transcript, timestamped_transcript, method, raw_segments = await asyncio.to_thread(
                smart_transcribe, req.url, video_id, progress_cb
            )

            yield sse_event("progress", {"step": "transcript_done", "message": "✅ Got transcript via YouTube API (instant!)"})

            # Step 3: Chunk
            yield sse_event("progress", {"step": "chunk", "message": "Chunking transcript..."})
            await asyncio.sleep(0)
            chunks = split_text(transcript)

            # Step 4: Embed & store
            yield sse_event("progress", {"step": "embed", "message": f"Embedding {len(chunks)} chunks into vector DB..."})
            await asyncio.sleep(0)
            faiss_store = await asyncio.to_thread(embed_and_store, video_id, chunks)

            # Step 5: Generate summary
            yield sse_event("progress", {"step": "summary", "message": "Generating summary..."})
            await asyncio.sleep(0)
            summary = await asyncio.to_thread(generate_summary, transcript, chunks, "detailed")

            # Save to store
            video_store[video_id] = {
                "transcript": transcript,
                "timestamped_transcript": timestamped_transcript,
                "summary": summary,
                "chunks": chunks,
                "metadata": metadata,
                "method": method,
                "faiss": faiss_store,
                "raw_segments": raw_segments,
            }

            yield sse_event("complete", {
                "video_id": video_id,
                "transcript": transcript,
                "timestamped_transcript": timestamped_transcript,
                "summary": summary,
                "method": method,
                "has_segments": len(raw_segments) > 0,
            })

        except Exception as e:
            yield sse_event("error", {"message": str(e)})

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/api/chat")
async def chat(req: ChatRequest):
    """RAG-based chat — streams response via SSE."""

    async def event_stream():
        try:
            if req.video_id not in video_store:
                yield sse_event("error", {"message": "Video not processed yet. Please process the video first."})
                return

            yield sse_event("progress", {"message": "Searching transcript..."})
            await asyncio.sleep(0)

            answer = await asyncio.to_thread(rag_answer, req.message, req.video_id)
            yield sse_event("answer", {"text": answer})

        except Exception as e:
            yield sse_event("error", {"message": str(e)})

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/api/segments/{video_id}")
async def get_segments(video_id: str):
    """Return raw transcript segments with timestamps for synced playback."""
    from fastapi.responses import JSONResponse
    if video_id not in video_store:
        return JSONResponse({"error": "Video not processed yet."}, status_code=404)
    segments = video_store[video_id].get("raw_segments", [])
    metadata = video_store[video_id].get("metadata", {})
    return JSONResponse({
        "video_id": video_id,
        "segments": segments,
        "duration": metadata.get("duration", 0),
        "title": metadata.get("title", ""),
    })


@app.post("/api/feature")
async def feature(req: FeatureRequest):
    """Generate additional features: chapters, concepts, mindmap, summary styles."""

    async def event_stream():
        try:
            if req.video_id not in video_store:
                yield sse_event("error", {"message": "Video not processed yet."})
                return

            transcript = video_store[req.video_id]["transcript"]
            chunks = video_store[req.video_id]["chunks"]

            yield sse_event("progress", {"message": f"Generating {req.feature}..."})
            await asyncio.sleep(0)

            if req.feature == "summary":
                result = await asyncio.to_thread(generate_summary, transcript, chunks, req.style or "detailed")
            elif req.feature == "chapters":
                result = await asyncio.to_thread(generate_chapters, transcript)
            elif req.feature == "concepts":
                result = await asyncio.to_thread(generate_key_concepts, transcript)
            elif req.feature == "mindmap":
                result = await asyncio.to_thread(generate_mindmap, transcript)
            elif req.feature == "notes":
                result = await asyncio.to_thread(generate_notes, transcript)
            else:
                result = "Unknown feature requested."

            yield sse_event("result", {"feature": req.feature, "text": result})

        except Exception as e:
            yield sse_event("error", {"message": str(e)})

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
