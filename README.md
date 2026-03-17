<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white" />
  <img src="https://img.shields.io/badge/FAISS-0467DF?style=for-the-badge&logo=meta&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</p>

<h1 align="center">🎬 YouTube Video Summarizer</h1>
<h3 align="center">Agentic RAG-Powered • Real-Time Streaming • AI Chat with Videos</h3>

<p align="center">
  Paste any YouTube link → Get AI summaries, chapters, mind maps, study notes, synced transcript playback, and chat with your video all in real-time.
</p>

---

## 📑 Table of Contents

- [📑 Table of Contents](#-table-of-contents)
- [🎥 Demo](#-demo)
- [🌟 Features at a Glance](#-features-at-a-glance)
- [⚡ How It Works (Simple)](#-how-it-works-simple)
- [🏗️ System Architecture](#️-system-architecture)
- [🔄 Video Processing Pipeline](#-video-processing-pipeline)
- [🤖 RAG (Retrieval-Augmented Generation) Flow](#-rag-retrieval-augmented-generation-flow)
- [📝 Map-Reduce Summarization](#-map-reduce-summarization)
- [▶️ Watch View — Synced Transcript](#️-watch-view--synced-transcript)
- [🕐 Watch History System](#-watch-history-system)
- [📂 Project Structure](#-project-structure)
- [🧩 Module-wise Division](#-module-wise-division)
  - [📥 Module 1 — Video Ingestion \& Data Extraction](#-module-1--video-ingestion--data-extraction)
  - [🧠 Module 2 — AI/ML Processing \& Summarization Engine](#-module-2--aiml-processing--summarization-engine)
  - [💬 Module 3 — RAG Chat \& Conversational AI](#-module-3--rag-chat--conversational-ai)
  - [🖥️ Module 4 — Frontend UI \& User Experience](#️-module-4--frontend-ui--user-experience)
  - [▶️ Module 5 — Watch View \& Synced Transcript Playback](#️-module-5--watch-view--synced-transcript-playback)
  - [⚙️ Module 6 — API Layer \& Backend Infrastructure](#️-module-6--api-layer--backend-infrastructure)
- [🛠️ Tech Stack](#️-tech-stack)
- [⚡ Performance](#-performance)
- [🚀 Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [1. Clone \& Install](#1-clone--install)
  - [2. Configure Environment](#2-configure-environment)
  - [3. Run](#3-run)
- [🌐 API Endpoints](#-api-endpoints)
  - [Request/Response Examples](#requestresponse-examples)
- [🖼️ UI Flow](#️-ui-flow)
- [📦 Deployment (Render)](#-deployment-render)
- [🔒 Security](#-security)
- [❓ FAQ](#-faq)
- [🗺️ Roadmap](#️-roadmap)
- [🤝 Contributing](#-contributing)
  - [Development Setup](#development-setup)
- [📄 License](#-license)
- [👨‍💻 Author](#-author)

---

## 🎥 Demo

<p align="center">
  <i>📸 Screenshots coming soon — run locally to see the full experience!</i>
</p>

> **Landing Page** → Paste URL → **Processing Screen** → **Main Dashboard** with Summary, Chapters, Mind Map, Notes, Transcript, AI Chat → **Watch View** with synced transcript → **History Panel**

---

## 🌟 Features at a Glance

| Feature | Description |
|---------|-------------|
| 📝 **AI Summary** | Map-Reduce style detailed summary with key takeaways |
| 📚 **Chapters** | Auto-generated chapter breakdown with time estimates |
| 🧠 **Key Concepts** | Extracted concepts, terms & people as a table |
| 🗺️ **Mind Map** | Hierarchical mind map of video content |
| 📒 **Study Notes** | Structured notes ready for revision |
| 💬 **AI Chat (RAG)** | Ask any question — answers from the video transcript |
| ▶️ **Watch + Synced Transcript** | Video player with live-highlighted transcript |
| 📊 **Watch Progress** | Track how much of the video you've watched (%) |
| 🕐 **Watch History** | Persistent history of all watched videos |
| 📄 **Export PDF** | Export any content as a formatted PDF |
| 🌓 **Dark / Light Mode** | Full theme support |

---

## ⚡ How It Works (Simple)

```mermaid
flowchart LR
    A["🔗 Paste\nYouTube URL"] --> B["📥 Fetch\nTranscript"]
    B --> C["✂️ Chunk\n& Embed"]
    C --> D["🧠 AI\nSummarize"]
    D --> E["✨ View Results\n& Chat"]

    style A fill:#7c6ef0,stroke:#7c6ef0,color:#fff,rx:12
    style B fill:#ec4899,stroke:#ec4899,color:#fff,rx:12
    style C fill:#f59e0b,stroke:#f59e0b,color:#fff,rx:12
    style D fill:#06b6d4,stroke:#06b6d4,color:#fff,rx:12
    style E fill:#6ee7a0,stroke:#6ee7a0,color:#000,rx:12
```

**5 simple steps:**

1. **Paste** any YouTube URL
2. **Transcript** is fetched instantly via YouTube's API (supports English & Hindi)
3. **Chunked** into overlapping segments and embedded into a FAISS vector database
4. **AI summarizes** using Map-Reduce over Groq's blazing-fast LLM
5. **Explore** — read summaries, watch with synced transcript, chat with RAG, export PDF

---

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph Client["🖥️ Browser (Frontend)"]
        UI[Landing Page]
        APP[Main App View]
        WATCH[Watch View]
        HIST[History Panel]
    end

    subgraph Server["⚙️ FastAPI Backend"]
        API[API Routes]
        PROC[Video Processor]
        RAG[RAG Engine]
        GEN[Content Generators]
    end

    subgraph External["🌐 External Services"]
        YT[YouTube API]
        GROQ[Groq LLM API]
        YTDLP[yt-dlp]
    end

    subgraph Storage["💾 Storage"]
        MEM[In-Memory Store]
        FAISS[FAISS Vector DB]
        LS[localStorage]
    end

    UI -->|YouTube URL| API
    API -->|SSE Stream| APP
    APP -->|Chat Query| RAG
    APP -->|Feature Request| GEN

    PROC -->|Fetch Transcript| YT
    PROC -->|Video Metadata| YTDLP
    PROC -->|Embed Chunks| FAISS
    PROC -->|Cache Data| MEM
    GEN -->|LLM Calls| GROQ
    RAG -->|Vector Search| FAISS
    RAG -->|Generate Answer| GROQ
    HIST -->|Persist History| LS

    style Client fill:#1a1a2e,stroke:#7c6ef0,color:#e8e6f0
    style Server fill:#12121a,stroke:#6ee7a0,color:#e8e6f0
    style External fill:#0a0a0f,stroke:#ec4899,color:#e8e6f0
    style Storage fill:#22223a,stroke:#f59e0b,color:#e8e6f0
```

---

## 🔄 Video Processing Pipeline

This is the core flow when a user pastes a YouTube URL and hits "Summarize":

```mermaid
flowchart TD
    A[🔗 User Pastes YouTube URL] --> B[Extract Video ID]
    B --> C[Fetch Metadata via yt-dlp]
    C --> D{Video Already Processed?}
    
    D -->|Yes| E[Return Cached Data]
    D -->|No| F[Fetch Transcript]
    
    F --> G{Manual Transcript Available?}
    G -->|Yes| H[Use Manual Transcript]
    G -->|No| I{Auto-Generated Available?}
    I -->|Yes| J[Use Auto-Generated]
    I -->|No| K{Any Language Available?}
    K -->|Yes| L[Use Any Available]
    K -->|No| M[❌ Error: No Transcript]
    
    H --> N[Parse Segments + Timestamps]
    J --> N
    L --> N
    
    N --> O[Split into Chunks<br/>1200 chars, 200 overlap]
    O --> P[Generate Embeddings<br/>all-MiniLM-L6-v2]
    P --> Q[Store in FAISS Vector DB]
    Q --> R[Map-Reduce Summary<br/>via Groq LLM]
    R --> S[✅ Stream Results via SSE]

    style A fill:#7c6ef0,stroke:#7c6ef0,color:#fff
    style S fill:#6ee7a0,stroke:#6ee7a0,color:#000
    style M fill:#f87171,stroke:#f87171,color:#fff
```

---

## 🤖 RAG (Retrieval-Augmented Generation) Flow

When a user asks a question in the AI Chat:

```mermaid
flowchart LR
    A[💬 User Question] --> B[Generate Query Embedding]
    B --> C[FAISS Similarity Search<br/>Top 5 Chunks]
    C --> D[Build Context from<br/>Retrieved Chunks]
    D --> E[Prompt Engineering<br/>Context + Question]
    E --> F[Groq LLM<br/>Generates Answer]
    F --> G[📨 Stream Answer via SSE]

    style A fill:#7c6ef0,stroke:#7c6ef0,color:#fff
    style G fill:#6ee7a0,stroke:#6ee7a0,color:#000
```

---

## 📝 Map-Reduce Summarization

The summary is generated using an agentic Map-Reduce pattern:

```mermaid
flowchart TD
    T[Full Transcript] --> S[Split into Chunks]
    
    S --> B1[Batch 1<br/>Chunks 1-3]
    S --> B2[Batch 2<br/>Chunks 4-6]
    S --> B3[Batch 3<br/>Chunks 7-9]
    S --> BN[Batch N<br/>...]
    
    B1 --> P1[Partial Summary 1]
    B2 --> P2[Partial Summary 2]
    B3 --> P3[Partial Summary 3]
    BN --> PN[Partial Summary N]
    
    P1 --> MERGE[🔗 Final Merge Prompt]
    P2 --> MERGE
    P3 --> MERGE
    PN --> MERGE
    
    MERGE --> FINAL["📋 Final Summary<br/>• Overview<br/>• Key Takeaways<br/>• Core Concepts Table<br/>• Conclusion"]

    style T fill:#7c6ef0,stroke:#7c6ef0,color:#fff
    style FINAL fill:#6ee7a0,stroke:#6ee7a0,color:#000
    style MERGE fill:#ec4899,stroke:#ec4899,color:#fff
```

---

## ▶️ Watch View — Synced Transcript

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant YT as YouTube Player
    participant API as Backend API

    U->>F: Click "Watch with Synced Transcript"
    F->>API: GET /api/segments/{video_id}
    API-->>F: Raw segments [{text, start, duration}, ...]
    F->>YT: Create YouTube IFrame Player
    F->>F: Render transcript segments

    loop Every 500ms
        F->>YT: getCurrentTime()
        YT-->>F: currentTime (seconds)
        F->>F: Highlight active segment
        F->>F: Auto-scroll transcript
        F->>F: Update progress bar (%)
        F->>F: Save to localStorage
    end

    U->>F: Click transcript segment
    F->>YT: seekTo(timestamp)
```

---

## 🕐 Watch History System

```mermaid
flowchart TD
    A[User Watches Video] --> B[Track Progress Every 500ms]
    B --> C[Calculate Max Watch %]
    C --> D[Save to localStorage<br/>Every 5 seconds]
    
    D --> E["History Entry:<br/>• videoId<br/>• title, channel<br/>• thumbnail URL<br/>• watchPct<br/>• lastWatched timestamp"]
    
    E --> F{Entry Exists?}
    F -->|Yes| G[Update with Higher %<br/>Move to Top]
    F -->|No| H[Add to Front]
    
    G --> I[Keep Max 50 Entries]
    H --> I
    
    I --> J[Display in History Panel]
    I --> K[Display on Landing Page<br/>Recent 6 Cards]
    
    J --> L[Click → Reload Video]
    K --> L

    style A fill:#7c6ef0,stroke:#7c6ef0,color:#fff
    style J fill:#6ee7a0,stroke:#6ee7a0,color:#000
    style K fill:#6ee7a0,stroke:#6ee7a0,color:#000
```

---

## 📂 Project Structure

```
📁 YouTube-Summarizer/
├── 📄 main.py                  # FastAPI backend — all routes, RAG, LLM logic
├── 📄 requirements.txt         # Python dependencies
├── 📄 render.yaml              # Render deployment config
├── 📄 .env                     # API keys (not in git)
├── 📄 .gitignore
├── 📁 templates/
│   └── 📄 index.html           # Full frontend — single page app
├── 📁 extra-files/             # Runtime files (FAISS index, etc.)
└── 📁 __pycache__/             # Python cache (ignored)
```

---

## 🧩 Module-wise Division

The project is organized into **6 core modules**, each handling a distinct responsibility layer — from data ingestion to user-facing interactions.

```mermaid
flowchart TD
    M1["📥 Module 1\nVideo Ingestion & Data Extraction"]
    M2["🧠 Module 2\nAI/ML Processing & Summarization"]
    M3["💬 Module 3\nRAG Chat & Conversational AI"]
    M6["⚙️ Module 6\nAPI Layer & Backend Infrastructure"]
    M4["🖥️ Module 4\nFrontend UI & User Experience"]
    M5["▶️ Module 5\nWatch View & Synced Playback"]

    M1 -->|Chunks & Segments| M2
    M2 -->|Vector Store| M3
    M2 -->|Generated Content| M6
    M3 -->|Answers| M6
    M6 -->|SSE Events| M4
    M6 -->|Segments API| M5
    M4 -.->|User Actions| M6
    M5 -.->|History Data| M4

    style M1 fill:#7c6ef0,stroke:#5b4cc4,color:#fff
    style M2 fill:#ec4899,stroke:#c9377e,color:#fff
    style M3 fill:#06b6d4,stroke:#0891a8,color:#fff
    style M4 fill:#f59e0b,stroke:#d68a09,color:#000
    style M5 fill:#6ee7a0,stroke:#4ade80,color:#000
    style M6 fill:#f87171,stroke:#dc5555,color:#fff
```

---

### 📥 Module 1 — Video Ingestion & Data Extraction

> *Handles everything from URL input to producing clean, chunked transcript data ready for AI processing.*

| # | Functionality | Description |
|:-:|---------------|-------------|
| 1 | **URL Parsing** | YouTube URL validation and video ID extraction |
| 2 | **Metadata Retrieval** | Fetch title, channel, thumbnail, and duration via yt-dlp |
| 3 | **Manual Transcript Fetch** | Priority fetch of human-written captions (English & Hindi) |
| 4 | **Auto-Caption Fallback** | Fallback to YouTube's auto-generated transcript |
| 5 | **Multi-Language Detection** | Detect and select best available transcript language |
| 6 | **Segment Parsing** | Parse raw transcript into timestamped segments with durations |
| 7 | **Text Chunking** | Split transcript into overlapping chunks (1200 chars, 200 overlap) |
| 8 | **Cache Detection** | Skip re-processing for already-processed videos |
| 9 | **Error Handling** | Graceful errors for invalid URLs or missing transcripts |
| 10 | **Segment API** | Serve raw segments via dedicated endpoint for playback sync |

---

### 🧠 Module 2 — AI/ML Processing & Summarization Engine

> *Core intelligence layer — embeds transcript chunks, builds vector indices, and generates all AI content.*

| # | Functionality | Description |
|:-:|---------------|-------------|
| 1 | **Embedding Generation** | Generate 384-dim vectors using HuggingFace all-MiniLM-L6-v2 |
| 2 | **FAISS Indexing** | Build and store vector database from transcript chunk embeddings |
| 3 | **Map-Reduce Summary** | Batch-wise partial summaries merged into a final comprehensive summary |
| 4 | **Summary Merging** | Final merge producing overview, key takeaways, and conclusion |
| 5 | **Chapter Generation** | Auto-generate chapter breakdowns with estimated timestamps |
| 6 | **Concept Extraction** | Extract key concepts, terms, and people as structured tables |
| 7 | **Mind Map Generation** | Produce hierarchical mind maps from video content |
| 8 | **Study Notes** | Generate structured, revision-ready study notes |
| 9 | **Prompt Engineering** | Tailored system prompts for each feature (summary, chapters, etc.) |
| 10 | **Groq LLM Integration** | Ultra-fast inference via Groq-hosted llama-3.3-70b model |

---

### 💬 Module 3 — RAG Chat & Conversational AI

> *Retrieval-Augmented Generation engine — lets users ask any question and get answers grounded in the video.*

| # | Functionality | Description |
|:-:|---------------|-------------|
| 1 | **Query Embedding** | Embed user questions using the same sentence-transformer model |
| 2 | **Similarity Search** | FAISS top-5 nearest-neighbor search over transcript chunks |
| 3 | **Context Construction** | Build a context window from the most relevant retrieved chunks |
| 4 | **Prompt Assembly** | Combine context + user question + system instructions into a prompt |
| 5 | **Streaming Generation** | Stream LLM-generated answers token-by-token via Groq |
| 6 | **SSE Delivery** | Real-time answer delivery to frontend via Server-Sent Events |
| 7 | **Chat History** | Maintain conversation history within a session |
| 8 | **Out-of-Scope Handling** | Gracefully decline questions not answerable from the transcript |
| 9 | **Isolated Vector Stores** | Per-video FAISS indices to avoid cross-video contamination |
| 10 | **Low-Latency Pipeline** | End-to-end response in ~2-3 seconds |

---

### 🖥️ Module 4 — Frontend UI & User Experience

> *Single-page application delivering a polished, responsive interface for all features.*

| # | Functionality | Description |
|:-:|---------------|-------------|
| 1 | **Landing Page** | URL input field with recent history cards for quick access |
| 2 | **Processing Screen** | Real-time progress indicators streamed via SSE |
| 3 | **Tabbed Dashboard** | Switchable tabs — Summary, Chapters, Concepts, Mind Map, Notes |
| 4 | **Chat Interface** | Interactive AI chat with styled message bubbles |
| 5 | **Theme Toggle** | Dark / Light mode with smooth CSS variable transitions |
| 6 | **PDF Export** | Export any content tab as a formatted PDF via html2pdf.js |
| 7 | **Markdown Rendering** | Render AI-generated Markdown content via marked.js |
| 8 | **Responsive Layout** | Adaptive design for desktop and tablet viewports |
| 9 | **Animations** | Smooth transitions, loading skeletons, and micro-interactions |
| 10 | **View Navigation** | Seamless flow: Landing → Processing → Dashboard → Watch |

---

### ▶️ Module 5 — Watch View & Synced Transcript Playback

> *Immersive video watching experience with live transcript sync and persistent progress tracking.*

| # | Functionality | Description |
|:-:|---------------|-------------|
| 1 | **YouTube Player** | Embedded YouTube IFrame player integration |
| 2 | **Live Transcript Sync** | Highlight active transcript segment in real-time (500ms polling) |
| 3 | **Auto-Scroll** | Transcript auto-scrolls to follow current playback position |
| 4 | **Click-to-Seek** | Click any transcript segment to jump to that point in the video |
| 5 | **Progress Bar** | Real-time watch progress indicator (percentage watched) |
| 6 | **Progress Persistence** | Save watch progress to localStorage every 5 seconds |
| 7 | **History Tracking** | Record title, channel, thumbnail, and timestamp per video |
| 8 | **History Panel** | Clickable history cards to reload and resume past videos |
| 9 | **LRU Management** | Maintain max 50 entries, newest first |
| 10 | **Recent Cards** | Display last 6 watched videos on the landing page |

---

### ⚙️ Module 6 — API Layer & Backend Infrastructure

> *The backbone — routing, streaming, validation, and deployment configuration.*

| # | Functionality | Description |
|:-:|---------------|-------------|
| 1 | **FastAPI Routes** | RESTful API design with clean route separation |
| 2 | **SSE Streaming** | Server-Sent Events for all long-running operations |
| 3 | **Pydantic Validation** | Request/response models with strict type checking |
| 4 | **In-Memory Cache** | Processed video data stored in memory for fast retrieval |
| 5 | **CORS Config** | Cross-origin access configuration for frontend requests |
| 6 | **Template Serving** | Static files and HTML templates via Jinja2 |
| 7 | **Env Management** | Secure API key loading via dotenv (.env file) |
| 8 | **Render Deployment** | One-click deploy config via render.yaml |
| 9 | **ASGI Server** | Uvicorn with hot-reload for development |
| 10 | **Error Handling** | Structured error responses and graceful exception management |

---

## 🛠️ Tech Stack

```mermaid
graph LR
    subgraph Frontend["🖥️ Frontend"]
        HTML["HTML5"]
        CSS["CSS3 + Variables"]
        JS["Vanilla JavaScript"]
        MARKED["marked.js"]
        PDF["html2pdf.js"]
        YTAPI["YouTube IFrame API"]
    end

    subgraph Backend["⚙️ Backend"]
        FAST["FastAPI"]
        SSE["Server-Sent Events"]
        LC["LangChain"]
        PYDANTIC["Pydantic"]
    end

    subgraph AIML["🧠 AI / ML"]
        GROQ["Groq LLM Inference"]
        HF["HuggingFace Embeddings"]
        FAISS["FAISS Vector Search"]
        MODEL["llama-3.3-70b"]
        EMBED["all-MiniLM-L6-v2"]
    end

    subgraph Data["📦 Data & APIs"]
        YTDLP["yt-dlp"]
        YTRANS["youtube-transcript-api"]
        LOCAL["localStorage"]
    end

    style Frontend fill:#1a1a2e,stroke:#7c6ef0,color:#e8e6f0
    style Backend fill:#12121a,stroke:#6ee7a0,color:#e8e6f0
    style AIML fill:#22223a,stroke:#ec4899,color:#e8e6f0
    style Data fill:#0a0a0f,stroke:#f59e0b,color:#e8e6f0
```

---

## ⚡ Performance

| Metric | Value |
|--------|-------|
| **Transcript Fetch** | ~1-2 seconds (YouTube API) |
| **Embedding** (avg video) | ~3-5 seconds |
| **Summary Generation** | ~5-10 seconds |
| **RAG Chat Response** | ~2-3 seconds |
| **Total Processing** | ~15-25 seconds (end-to-end) |
| **Embedding Model** | all-MiniLM-L6-v2 (384 dims) |
| **LLM** | Groq-hosted (ultra-fast inference) |
| **Chunk Size** | 1200 chars, 200 overlap |
| **Vector Search** | Top-5 similarity (FAISS) |

> 💡 Groq provides the fastest LLM inference available — responses are near-instant compared to traditional cloud LLMs.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- [Groq API Key](https://console.groq.com/) (free)

### 1. Clone & Install

```bash
git clone https://github.com/divye07/SWE-Proj.git
cd SWE-Proj
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run

```bash
python main.py
```

Open **http://localhost:8000** in your browser. 🎉

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serve the frontend |
| `POST` | `/api/process` | Process a YouTube video (SSE stream) |
| `POST` | `/api/chat` | RAG-based Q&A chat (SSE stream) |
| `POST` | `/api/feature` | Generate summary/chapters/concepts/mindmap/notes (SSE stream) |
| `GET` | `/api/segments/{video_id}` | Get raw transcript segments for synced playback |

### Request/Response Examples

<details>
<summary><b>POST /api/process</b></summary>

**Request:**
```json
{ "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ" }
```

**SSE Events:**
```
event: progress
data: {"step": "metadata", "message": "Fetching video info..."}

event: metadata
data: {"video_id": "dQw4w9WgXcQ", "title": "...", "channel": "...", ...}

event: progress
data: {"step": "summary", "message": "Generating summary..."}

event: complete
data: {"video_id": "...", "transcript": "...", "summary": "...", ...}
```
</details>

<details>
<summary><b>POST /api/chat</b></summary>

**Request:**
```json
{ "video_id": "dQw4w9WgXcQ", "message": "What is the main topic?" }
```

**SSE Events:**
```
event: answer
data: {"text": "The main topic of this video is..."}
```
</details>

---

## 🖼️ UI Flow

```mermaid
stateDiagram-v2
    [*] --> Landing: Open App
    
    Landing --> Processing: Paste URL + Click Summarize
    Landing --> Processing: Click History Card
    
    Processing --> MainApp: ✅ Done
    Processing --> Landing: ❌ Error
    
    MainApp --> MainApp: Switch Tabs<br/>(Summary/Chapters/Concepts/MindMap/Notes)
    MainApp --> MainApp: AI Chat
    MainApp --> WatchView: Click "Watch with Synced Transcript"
    MainApp --> HistoryPanel: Click "History"
    MainApp --> Landing: Click "Home"
    
    WatchView --> MainApp: Click "Back"
    HistoryPanel --> MainApp: Close Panel
    HistoryPanel --> Processing: Click History Item
```

---

## 📦 Deployment (Render)

This project includes a `render.yaml` for one-click deployment:

1. Push to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your repo
4. Add environment variables: `GROQ_API_KEY`
5. Deploy! 🚀

**Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## 🔒 Security

- API keys stored in `.env` (excluded from git via `.gitignore`)
- No user data stored on server — watch history is client-side only (localStorage)
- Input validation via Pydantic models
- HTML escaping for all user-facing content

---

## ❓ FAQ

<details>
<summary><b>Q: Does it work with any YouTube video?</b></summary>

It works with any video that has subtitles/captions (manual or auto-generated). Most English and Hindi videos have auto-generated captions enabled by YouTube.
</details>

<details>
<summary><b>Q: Is it free to use?</b></summary>

Yes! Groq offers a generous free tier. The embedding model runs locally. No paid APIs required.
</details>

<details>
<summary><b>Q: Can I use it for videos in other languages?</b></summary>

Currently optimized for English and Hindi transcripts. If a video has captions in another language, it will still attempt to use them.
</details>

<details>
<summary><b>Q: Where is watch history stored?</b></summary>

Watch history is stored in your browser's localStorage — nothing is sent to any server. Clearing browser data will reset it.
</details>

<details>
<summary><b>Q: Why is the summary taking long?</b></summary>

Longer videos produce more chunks, which means more LLM calls during Map-Reduce summarization. Groq is already the fastest — typical videos process in 15-25 seconds.
</details>

<details>
<summary><b>Q: Can I deploy this for free?</b></summary>

Yes! Render.com offers a free tier that's perfect for this app. See the <a href="#-deployment-render">Deployment</a> section.
</details>

---

## 🗺️ Roadmap

```mermaid
gantt
    title Feature Roadmap
    dateFormat YYYY-MM
    section Done ✅
        AI Summary & RAG Chat        :done, 2026-01, 2026-02
        Chapters, Concepts, Mind Map  :done, 2026-02, 2026-02
        Study Notes & PDF Export      :done, 2026-02, 2026-03
        Watch View + Synced Transcript:done, 2026-03, 2026-03
        Watch Progress & History      :done, 2026-03, 2026-03
    section Planned 🚧
        Multi-language Support        :active, 2026-04, 2026-05
        Playlist Batch Processing     :2026-04, 2026-06
        User Accounts & Cloud Sync    :2026-05, 2026-07
        Chrome Extension              :2026-06, 2026-08
        Mobile Responsive Overhaul    :2026-06, 2026-07
        Collaborative Notes           :2026-07, 2026-09
```

**Coming Next:**
- 🌍 Multi-language transcript support (auto-translate)
- 📋 Playlist batch processing — summarize entire playlists
- 👤 User accounts with cloud-synced history
- 🧩 Chrome extension — summarize directly from YouTube
- 📱 Full mobile-responsive redesign
- 👥 Collaborative notes & shared summaries

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup

```bash
git clone https://github.com/divye07/SWE-Proj.git
cd SWE-Proj
pip install -r requirements.txt
# Add your .env file with GROQ_API_KEY
python main.py
# App runs on http://localhost:8000 with hot-reload
```

---

## 📄 License

**⚠️ All Rights Reserved** — This project is proprietary. No part of this software may be copied, modified, distributed, or used without explicit written permission from the author. See [LICENSE](LICENSE) for full terms.

---

## 👨‍💻 Author

**Divye** — [GitHub](https://github.com/divye07)
**Sachin** — [GitHub](https://github.com/sachinvv552)
**Devang** — [GitHub](https://github.com/Devang0124)

---

<p align="center">
  <b>⭐ Star this repo if you found it useful!</b>
</p>
