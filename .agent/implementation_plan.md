# 🎭 Implementation Plan: Professional Frontend
## Automated Auditorium Lighting System

**Status:** READY TO BUILD  
**Date:** 2026-02-18  
**Stack:** React (Vite) + Tailwind CSS v3 + FastAPI  

---

## 📋 Decisions Locked

| Decision | Choice |
|---|---|
| Frontend Framework | React (Vite) |
| Styling | Tailwind CSS v3 |
| Backend | FastAPI (Python) |
| Real-time | WebSocket (progress + simulation) |
| History | No — one-shot (upload → process → simulate) |
| Simulation | Opens as **separate full-screen page** (not iframe) |
| Authentication | None |
| Location | `frontend/` and `backend/` at project root |

---

## 🏗️ Architecture

```
                    ┌──────────────────────────┐
                    │     React Frontend       │
                    │   (localhost:5173)        │
                    │                          │
                    │  Landing → Upload →      │
                    │  Processing → Results    │
                    └──────────┬───────────────┘
                               │ REST + WebSocket
                               ▼
                    ┌──────────────────────────┐
                    │     FastAPI Backend       │
                    │   (localhost:8000)        │
                    │                          │
                    │  POST /api/upload         │
                    │  WS   /ws/progress/{id}   │
                    │  GET  /api/results/{id}    │
                    └──────────┬───────────────┘
                               │ Calls existing phases
                               ▼
              ┌─────────────────────────────────┐
              │  Phase 1 → 2 → 3 → 4 → 6       │
              │  (Existing Python pipeline)      │
              └─────────────────────────────────┘
                               │
                               ▼ Generates lighting_instructions.json
              ┌─────────────────────────────────┐
              │  3D Simulation (module_1)        │
              │  (localhost:8081) separate page   │
              └─────────────────────────────────┘
```

---

## 📁 File Structure

```
Automated_Audiotorium_Lightning_Ram/
│
├── frontend/                          # 🆕 React + Tailwind
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/                    # Reusable UI atoms
│   │   │   │   ├── Button.jsx         # Glowing CTA buttons
│   │   │   │   ├── Card.jsx           # Glass-morphism cards
│   │   │   │   ├── ProgressBar.jsx    # Animated gradient bar
│   │   │   │   ├── FileDropZone.jsx   # Drag & drop area
│   │   │   │   ├── PhaseStep.jsx      # Single phase status row
│   │   │   │   └── ParticleBackground.jsx  # Canvas particle animation
│   │   │   ├── layout/
│   │   │   │   ├── Header.jsx         # Top nav with project branding
│   │   │   │   └── PageTransition.jsx # Fade/slide transitions
│   │   │   └── charts/
│   │   │       ├── EmotionDonut.jsx   # Emotion distribution chart
│   │   │       └── EmotionTimeline.jsx # Scene-by-scene emotion bar
│   │   ├── pages/
│   │   │   ├── LandingPage.jsx        # Hero + features
│   │   │   ├── UploadPage.jsx         # Drag-drop + preview
│   │   │   ├── ProcessingPage.jsx     # Real-time pipeline dashboard
│   │   │   └── ResultsPage.jsx        # Summary + launch button
│   │   ├── hooks/
│   │   │   ├── useWebSocket.js        # WebSocket connection hook
│   │   │   └── useFileUpload.js       # File upload + validation hook
│   │   ├── utils/
│   │   │   └── api.js                 # API helper functions
│   │   ├── App.jsx                    # Router setup
│   │   ├── main.jsx                   # Entry point
│   │   └── index.css                  # Tailwind imports + custom styles
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── vite.config.js
│
├── backend/                           # 🆕 FastAPI server
│   ├── app.py                         # Main FastAPI application
│   ├── pipeline_runner.py             # Async wrapper for Phase 1→6
│   ├── websocket_manager.py           # WebSocket connection manager
│   └── requirements.txt              # fastapi, uvicorn, python-multipart, websockets
│
├── phase_1/                           # ✅ Existing — untouched
├── phase_2/                           # ✅ Existing — untouched
├── phase_3/                           # ✅ Existing — untouched
├── phase_4/                           # ✅ Existing — untouched
├── phase_5/                           # ✅ Existing — untouched
├── phase_6/                           # ✅ Existing — untouched
├── data/                              # ✅ Existing — pipeline reads/writes here
├── external_simulation_prototype/     # ✅ Existing — simulation stays here
│   ├── module_1/                      # 3D auditorium (Three.js)
│   └── test_controller.py            # WebSocket controller
├── config.py                          # ✅ Existing
├── main.py                            # ✅ Existing pipeline entry
└── README.md
```

---

## 📱 Screen Specifications

### Screen 1: Landing Page (`/`)

**Purpose:** First impression. Establish the product identity.

**Layout:**
```
┌──────────────────────────────────────────────────┐
│  [Header: Logo + "Automated Auditorium Lighting"]│
│                                                   │
│          ✦ Animated spotlight particles ✦         │
│                                                   │
│        🎭 AUTOMATED AUDITORIUM LIGHTING           │
│      AI-Powered Theatre Lighting Design           │
│    From Script to Stage — In Seconds              │
│                                                   │
│         [ ✨ Upload Your Script → ]               │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ 🎭 AI     │  │ 💡 Smart  │  │ 🎬 3D     │       │
│  │ Emotion   │  │ Lighting  │  │ Visual   │       │
│  │ Analysis  │  │ Design   │  │ ization  │       │
│  │           │  │          │  │          │       │
│  │ DistilRo- │  │ RAG +    │  │ Three.js │       │
│  │ BERTa ML  │  │ LangChain│  │ WebGL    │       │
│  └──────────┘  └──────────┘  └──────────┘       │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │  HOW IT WORKS                                │ │
│  │  1. Upload Script → 2. AI Processes →       │ │
│  │  3. View 3D Simulation                       │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  Supports: PDF • TXT • DOCX                      │
└──────────────────────────────────────────────────┘
```

**Components used:** `ParticleBackground`, `Button`, `Card`, `Header`

**Animations:**
- Particle canvas in background (subtle floating light dots)
- Title text: typewriter effect or glow-in
- Feature cards: stagger fade-in from bottom (200ms delay each)
- CTA button: pulsing glow ring

**Tailwind classes (key):**
- Background: `bg-[#0a0a1a]`
- Cards: `bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl`
- Button: `bg-gradient-to-r from-amber-500 to-yellow-400 hover:shadow-[0_0_30px_rgba(255,215,0,0.3)]`

---

### Screen 2: Upload Page (`/upload`)

**Purpose:** Accept the script file with a beautiful drag-drop experience.

**Layout:**
```
┌──────────────────────────────────────────────────┐
│  [Header: ← Back    "Upload Script"]             │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │                                              │ │
│  │     ┌────────────────────────────┐          │ │
│  │     │    📄                       │          │ │
│  │     │                            │          │ │
│  │     │   Drag & Drop your script  │          │ │
│  │     │   or click to browse       │          │ │
│  │     │                            │          │ │
│  │     │   PDF • TXT • DOCX         │          │ │
│  │     └────────────────────────────┘          │ │
│  │                                              │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  ┌─ FILE PREVIEW (appears after upload) ───────┐ │
│  │  📄 Script-2.txt  │  4.2 KB  │  TXT ✅      │ │
│  │                                              │ │
│  │  "SCENE 1: THE LOCKED ROOM                  │ │
│  │   A dimly lit room. The door is sealed..."   │ │
│  │                                              │ │
│  │  Script Title: [ The Room That Remembers  ]  │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│         [ 🚀 Begin Processing → ]                │
└──────────────────────────────────────────────────┘
```

**Components used:** `FileDropZone`, `Button`, `Card`

**Behavior:**
1. User drags file → border glows gold, icon scales up
2. File validates format on drop (PDF/TXT/DOCX only)
3. Preview panel slides in showing: filename, size, format badge, first 5 lines
4. Script title auto-detected from filename (editable input)
5. "Begin Processing" button appears
6. On click → POST `/api/upload` → receive `job_id` → navigate to `/processing/{job_id}`

**Animations:**
- Drop zone: dashed border rotation on drag-over
- File icon: bounce animation on successful drop
- Preview: slide-up reveal
- Invalid format: shake animation + red flash

---

### Screen 3: Processing Dashboard (`/processing/:jobId`)

**Purpose:** Show real-time pipeline progress. THE KEY SCREEN.

**Layout:**
```
┌──────────────────────────────────────────────────┐
│  [Header: "Processing: The Room That Remembers"] │
│                                                   │
│  ┌─ OVERALL PROGRESS ─────────────────────────┐ │
│  │  ████████████████████░░░░░░░░░  67%         │ │
│  │  Estimated: ~12 seconds remaining            │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  ┌─ PIPELINE STATUS ──────────────────────────┐  │
│  │                                             │  │
│  │  ✅ Phase 1: Script Parsing        2.3s     │  │
│  │     159 lines • 17 scenes • Screenplay      │  │
│  │                                             │  │
│  │  ✅ Phase 2: Emotion Analysis      4.1s     │  │
│  │     joy: 3 • fear: 4 • anger: 2             │  │
│  │                                             │  │
│  │  ✅ Phase 3: Knowledge Retrieval   1.8s     │  │
│  │     12 design rules loaded                  │  │
│  │                                             │  │
│  │  🔄 Phase 4: Lighting Design       ...      │  │
│  │     Generating scene 12 of 17...            │  │
│  │                                             │  │
│  │  ⏳ Phase 5: Preparing Simulation           │  │
│  │                                             │  │
│  │  ⏳ Phase 6: Validating Cues                │  │
│  │                                             │  │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  ┌─ LIVE STATS ───────────────────────────────┐  │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ │  │
│  │  │😊   │ │😨   │ │😡   │ │😢   │ │😐   │ │  │
│  │  │ JOY │ │FEAR │ │ANGER│ │SAD  │ │NEUT │ │  │
│  │  │  3  │ │  4  │ │  2  │ │  1  │ │  7  │ │  │
│  │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ │  │
│  └─────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

**Components used:** `ProgressBar`, `PhaseStep`, `Card`

**WebSocket flow:**
```
React connects to: ws://localhost:8000/ws/progress/{job_id}

Server sends:
→ {"phase": 1, "status": "running",  "detail": "Parsing script..."}
→ {"phase": 1, "status": "complete", "duration": 2.3, "stats": {"lines": 159, "scenes": 17}}
→ {"phase": 2, "status": "running",  "detail": "Analyzing scene 3/17..."}
→ {"phase": 2, "status": "complete", "duration": 4.1, "stats": {"joy": 3, "fear": 4, ...}}
→ {"phase": 3, "status": "running",  "detail": "Loading RAG indexes..."}
→ ...
→ {"phase": 6, "status": "complete", "redirect": "/results/{job_id}"}
```

**PhaseStep component states:**
| State | Icon | Style |
|---|---|---|
| `pending` | ⏳ | `text-gray-500 opacity-50` |
| `running` | 🔄 (spinning) | `text-amber-400 animate-pulse` + spinner |
| `complete` | ✅ | `text-green-400` + slide-in stats |
| `error` | ❌ | `text-red-400` + error message |

**Animations:**
- Progress bar: gradient shimmer sweep (CSS keyframe)
- Phase completion: checkmark SVG draw animation
- Stats cards: pop-in with scale transform
- On all complete: 3-second countdown overlay "Launching Simulation... 3... 2... 1..."

---

### Screen 4: Results Page (`/results/:jobId`)

**Purpose:** Quick summary before launching the simulation.

**Layout:**
```
┌──────────────────────────────────────────────────┐
│  [Header: "Analysis Complete ✨"]                │
│                                                   │
│  ┌────────────────┐  ┌────────────────────────┐  │
│  │   SCRIPT INFO  │  │   EMOTION BREAKDOWN    │  │
│  │                │  │                        │  │
│  │ 📄 Script-2    │  │     ┌──────────┐       │  │
│  │ 📝 17 scenes   │  │     │  DONUT   │       │  │
│  │ ⏱  8m 30s     │  │     │  CHART   │       │  │
│  │ 🎭 Drama      │  │     │          │       │  │
│  │                │  │     └──────────┘       │  │
│  └────────────────┘  │  joy: 18% fear: 24%   │  │
│                       │  anger: 12% neutral: 41% │
│  ┌────────────────┐  └────────────────────────┘  │
│  │  LIGHTING      │                              │
│  │  17 cues       │                              │
│  │  6 transitions │                              │
│  │  3 smoke FX    │                              │
│  │                │                              │
│  │ [📥 Download]  │                              │
│  └────────────────┘                              │
│                                                   │
│         [ 🎭 Launch 3D Simulation → ]            │
│                                                   │
└──────────────────────────────────────────────────┘
```

**Components used:** `Card`, `EmotionDonut`, `Button`

**Behavior:**
- Shows summary stats from all phases
- "Download" button → downloads `lighting_instructions.json`
- "Launch 3D Simulation" →
  1. Starts the simulation servers (HTTP + WebSocket) in background via API call
  2. Opens `http://localhost:8081` in a **new browser tab** (full-screen)
- Auto-launch option: redirects after 5s countdown

---

## 🔌 Backend API Specification

### `backend/app.py` — FastAPI Server

```
PORT: 8000

Endpoints:
──────────

POST /api/upload
  Body: multipart/form-data { file, title? }
  Response: { job_id: "abc123", filename: "Script-2.txt", format: "txt" }
  Action: Saves file to /tmp/uploads/{job_id}/, returns ID

WS /ws/progress/{job_id}
  Direction: Server → Client (push only)
  Messages: JSON objects with phase, status, detail, stats, duration
  Final message includes: { phase: "done", redirect: "/results/{job_id}" }

GET /api/results/{job_id}
  Response: {
    script: { title, format, scenes, duration },
    emotions: { distribution, dominant },
    lighting: { total_cues, transitions, smoke_count },
    instructions_path: "..."
  }

POST /api/launch/{job_id}
  Action: 
    1. Copies generated lighting_instructions.json to simulation data dir
    2. Starts module_1 HTTP server (port 8081) if not running
    3. Starts test_controller.py WebSocket server (port 8765) if not running
  Response: { simulation_url: "http://localhost:8081" }

GET /api/download/{job_id}
  Response: lighting_instructions.json file download
```

### `backend/pipeline_runner.py` — Async Pipeline

```python
# Conceptual structure:

async def run_pipeline(job_id: str, filepath: str, ws_callback):
    """
    Runs Phase 1 → 2 → 3 → 4 → 6 sequentially,
    sending progress updates via WebSocket after each step.
    """
    
    # Phase 1: Parse Script
    await ws_callback(phase=1, status="running", detail="Parsing script...")
    result_1 = phase_1_parse(filepath)      # Calls existing main.py logic
    await ws_callback(phase=1, status="complete", stats=result_1.stats)
    
    # Phase 2: Emotion Analysis
    await ws_callback(phase=2, status="running", detail="Loading ML model...")
    result_2 = phase_2_emotions(result_1)   # Calls existing emotion_analyzer
    await ws_callback(phase=2, status="complete", stats=result_2.distribution)
    
    # Phase 3: RAG Knowledge
    await ws_callback(phase=3, status="running", detail="Loading knowledge base...")
    result_3 = phase_3_rag(result_2)        # Calls existing rag_retriever
    await ws_callback(phase=3, status="complete", stats=result_3.stats)
    
    # Phase 4: Lighting Decision
    await ws_callback(phase=4, status="running", detail="Generating lighting...")
    result_4 = phase_4_decisions(result_2, result_3)  # Calls existing engine
    await ws_callback(phase=4, status="complete", stats=result_4.stats)
    
    # Phase 6: Validation
    await ws_callback(phase=6, status="running", detail="Validating cues...")
    result_6 = phase_6_validate(result_4)   # Calls existing validator
    await ws_callback(phase=6, status="complete", stats=result_6.stats)
    
    # Save lighting_instructions.json
    save_instructions(job_id, result_4)
    
    await ws_callback(phase="done", redirect=f"/results/{job_id}")
```

Key: This wraps your EXISTING phase code — we're not rewriting any ML or pipeline logic.

---

## 🎨 Design System (Tailwind)

### tailwind.config.js extensions

```javascript
theme: {
  extend: {
    colors: {
      stage: {
        bg:      '#0a0a1a',     // Deep dark background
        surface: '#1a1a2e',     // Card/panel surface
        border:  'rgba(255,255,255,0.1)',
        gold:    '#FFD700',     // Spotlight accent
        amber:   '#FFB347',     // Warm accent
        blue:    '#4A90E2',     // Cool accent
      }
    },
    fontFamily: {
      display: ['Outfit', 'sans-serif'],
      body:    ['Inter', 'sans-serif'],
      mono:    ['JetBrains Mono', 'monospace'],
    },
    animation: {
      'shimmer': 'shimmer 2s infinite',
      'glow':    'glow 2s ease-in-out infinite alternate',
      'float':   'float 6s ease-in-out infinite',
      'draw':    'draw 0.5s ease-out forwards',
    }
  }
}
```

### Glass-morphism card pattern
```
className="bg-white/5 backdrop-blur-md border border-white/10 
           rounded-2xl p-6 shadow-xl hover:bg-white/[0.08] 
           transition-all duration-300"
```

### Glowing button pattern
```
className="bg-gradient-to-r from-amber-500 to-yellow-400 
           text-black font-semibold px-8 py-3 rounded-full 
           hover:shadow-[0_0_30px_rgba(255,215,0,0.4)] 
           transition-all duration-300 hover:scale-105"
```

---

## 🔨 Build Order (Step by Step)

| Step | Task | Details | Est. Time |
|---|---|---|---|
| **1** | Scaffold React + Tailwind | `npx create-vite` + Tailwind v3 setup + design tokens | 15 min |
| **2** | Build reusable UI components | `Button`, `Card`, `ProgressBar`, `PhaseStep`, `ParticleBackground` | 40 min |
| **3** | Landing Page | Hero section, feature cards, animations, navigation | 30 min |
| **4** | Upload Page | `FileDropZone`, file validation, preview panel | 30 min |
| **5** | FastAPI backend setup | Server scaffold, upload endpoint, file storage | 25 min |
| **6** | Pipeline runner | Async wrapper calling Phase 1→6 with progress callbacks | 40 min |
| **7** | Processing Page | WebSocket hook, PhaseStep timeline, live stats | 40 min |
| **8** | Results Page | Summary cards, emotion chart, download button | 25 min |
| **9** | Simulation launcher | API endpoint to start simulation servers + redirect | 20 min |
| **10** | Polish | Page transitions, error states, loading skeletons, responsive | 30 min |
| | **TOTAL** | | **~4.5 hours** |

---

## ⚡ Key Technical Notes

1. **CORS:** FastAPI backend needs CORS middleware to accept requests from Vite dev server (localhost:5173 → localhost:8000)

2. **File Upload:** Uses `python-multipart` for FastAPI file handling. Max size: 10MB.

3. **Pipeline Integration:** The `pipeline_runner.py` imports directly from existing `phase_1/`, `phase_2/`, etc. — NO code duplication.

4. **Simulation Launch Flow:**
   - React calls `POST /api/launch/{job_id}`
   - Backend copies generated `lighting_instructions.json` to the simulation data directory
   - Backend starts `python3 -m http.server 8081` for module_1
   - Backend starts `python3 test_controller.py` for WebSocket
   - Returns URL → React opens new tab → Full-screen 3D simulation

5. **Error Handling:** If any phase fails, WebSocket sends `{phase: N, status: "error", message: "..."}` and the Processing page shows a retry button.

6. **Production Build:** `npm run build` in `frontend/` generates static files that FastAPI can serve directly via `StaticFiles` mount — single server deployment.
