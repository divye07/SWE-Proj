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
  Paste any YouTube link → Get AI summaries, chapters, mind maps, study notes, synced transcript playback, and chat with your video — all in real-time.
</p>

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
    GEN -->|LLM Calls| GROQ
    RAG -->|Vector Search| FAISS
    RAG -->|Generate Answer| GROQ

    MEM -->|Store Video Data| PROC
    LS -->|Watch History| HIST

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

## 🛠️ Tech Stack

```mermaid
graph LR
    subgraph Frontend
        HTML[HTML5]
        CSS[CSS3 + CSS Variables]
        JS[Vanilla JavaScript]
        MARKED[marked.js — Markdown]
        PDF[html2pdf.js — PDF Export]
        YTAPI[YouTube IFrame API]
    end

    subgraph Backend
        FAST[FastAPI]
        SSE[Server-Sent Events]
        LC[LangChain]
        PYDANTIC[Pydantic]
    end

    subgraph AI/ML
        GROQ[Groq — LLM Inference]
        HF[HuggingFace Embeddings]
        FAISS[FAISS — Vector Search]
        MODEL["LLM: llama-3.3-70b"]
        EMBED["Embed: all-MiniLM-L6-v2"]
    end

    subgraph Data
        YTDLP[yt-dlp — Metadata]
        YTRANS[youtube-transcript-api]
        LOCAL[localStorage — History]
    end

    style Frontend fill:#1a1a2e,stroke:#7c6ef0,color:#e8e6f0
    style Backend fill:#12121a,stroke:#6ee7a0,color:#e8e6f0
    style AI/ML fill:#22223a,stroke:#ec4899,color:#e8e6f0
    style Data fill:#0a0a0f,stroke:#f59e0b,color:#e8e6f0
```

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

## 👨‍💻 Author

**Divye** — [GitHub](https://github.com/divye07)

---

<p align="center">
  <b>⭐ Star this repo if you found it useful!</b>
</p>
