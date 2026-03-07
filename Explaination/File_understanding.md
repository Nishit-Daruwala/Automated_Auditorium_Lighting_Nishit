# 📂 Project File Understanding

This document provides a simple, 4-5 line explanation for every core Python file in the Automated Auditorium Lighting project. It explains what each file does and why it's needed in the overall workflow.

---

## 🏗️ Root Directory Files

### `main.py`
- **What it does:** The primary master script that orchestrates the entire pipeline from start to finish. It reads the input script (TXT/PDF/DOCX) and passes it through the various phases (Parsing, Emotion, RAG, Generation).
- **Why we need it:** It acts as the single central entry point for a user to process a raw theater script into a standardized, lighting-ready format.

### `main_phase2.py`
- **What it does:** Specifically handles the cue generation portion (originally Phase 4, historically named Phase 2 in some legacy pipelines). It takes processed scenes from Phase 1 and utilizes the Cue Generator to create lighting parameters.
- **Why we need it:** Allows developers to skip the heavy script-processing phase and jump directly into testing lighting generation logic if the script is already parsed.

### `app.py`
- **What it does:** Runs the FastAPI web server to host the 3D Lighting Visualizer (Phase 5). It manages WebSockets to broadcast real-time lighting cues to the frontend and handles OSC connections.
- **Why we need it:** This is the bridge that allows users to actually "see" the generated AI lighting design play out in a web browser instead of just reading JSON code.

### `config.py`
- **What it does:** Contains all the global settings, passwords, file paths, and tunable numbers (like max words per scene, LLM temperatures, or API keys).
- **Why we need it:** Prevents hardcoding values across 50 different files. If we want to change the LLM model or the fade duration, we only have to change it here.

### `run_diagnostics.py`
- **What it does:** A robust testing script that scans the entire project for missing folders, broken installations, missing API keys, or database errors.
- **Why we need it:** Helps quickly debug the system environment before a presentation or deployment to ensure everything is mechanically ready to run.

---

## 📜 Phase 1: Script & Scene Structure Processing

### `__init__.py`
- **What it does:** The main orchestrator for Phase 1. It receives the script path and chains together text acquisition, segmentation, and JSON building.
- **Why we need it:** Provides a clean interface (`run_phase_1`) so main.py doesn't have to call 10 different sub-scripts manually.

### `text_acquisition.py`
- **What it does:** Safely reads the text from the provided file path, utilizing OCR if necessary.
- **Why we need it:** Essential for getting the raw story text into the computer's memory to start the analysis process.

### `immutable_structurer.py` / `chunk_preprocessor.py`
- **What it does:** Locks the raw text into an unchangeable format (`ImmutableText`) and chunks it into overlapping pieces.
- **Why we need it:** We need coordinate systems for the text so we don't accidentally lose or duplicate words when giving heavy scripts to AI models.

### `llm_scene_segmenter.py`
- **What it does:** Uses AI (Llama/Local LLMs) to read the script chunks and logically chop them into distinct theatrical "scenes" (Action, Dialogue, etc.).
- **Why we need it:** Lighting needs to change per scene. This script automatically figures out where one scene ends and the next begins.

### `timestamp_engine.py` / `validation_layer.py`
- **What it does:** Calculates how many seconds each scene will take to act out on stage and strictly validates that scenes don't overlap.
- **Why we need it:** For the live simulation (Phase 5) to know exactly when to trigger the next lighting cue in real-time.

### `scene_json_builder.py` / `compat.py`
- **What it does:** Packages all the segmented, timestamped scenes into strict JSON formats and maintains backward compatibility.
- **Why we need it:** Ensures downstream phases (like Phase 2 Emotion) receive cleanly formatted data they can easily parse without crashing.

---

## 🎭 Phase 2: Emotion Analysis Module

### `__init__.py`
- **What it does:** The export module that exposes the `analyze_emotion` function for the rest of the pipeline to consume.
- **Why we need it:** Keeps the module boundaries clean and handles backward compatibility for older script formats.

### `emotion_analyzer.py`
- **What it does:** Uses AI models (Llama 3 Instruct or DistilRoBERTa) to read a segmented scene and determine its primary, secondary, and accent emotions (e.g., Joy, Tension, Fear).
- **Why we need it:** This is the core "brain" of the lighting design. The entire color and intensity logic in Phase 4 requires knowing how the scene "feels" first.

---

## 🧠 Phase 3: Knowledge Layer (Dual RAG)

### `__init__.py`
- **What it does:** Exposes the `get_retriever()` function to boot up the Knowledge Base database.
- **Why we need it:** Acts as the entry point for Phase 4 to ask questions to the database.

### `rag_retriever.py`
- **What it does:** Uses FAISS and LangChain to search internal databases for specific hardware constraints and professional lighting design rules matching the scene's emotion.
- **Why we need it:** Without this, the AI would guess random colors. This forces the AI to base its decisions on actual theatrical textbook rules.

### `ingestion/knowledge_ingestion.py`
- **What it does:** A script that converts our raw JSON rulebooks (Auditorium setups and lighting rules) into binary mathematical databases (FAISS vector stores).
- **Why we need it:** We have to run this once to build the database so the `rag_retriever` can instantly search through it later.

### `extract_book_rules.py`
- **What it does:** A helper script that reads literal PDF textbooks on stage lighting and rips out the core sentence rules.
- **Why we need it:** This is how we made the AI "smart" at lighting design—by feeding it actual university-level textbook logic.

---

## 💡 Phase 4: LLM Lighting Decision Engine

### `__init__.py`
- **What it does:** Exposes the `LightingDecisionEngine`, acting as the control panel for Phase 4 generation.
- **Why we need it:** Makes it easy for `main.py` to command the generation of semantic lighting instructions in bulk.

### `lighting_decision_engine.py`
- **What it does:** Takes the Emotion (from Phase 2) and the Design Rules (from Phase 3), gives them to an LLM, and forces the LLM to output Semantic Intents (e.g., Color=Red, Target=Front Wash).
- **Why we need it:** This translates the abstract "Sadness" of a script into physical, actionable lighting instructions for the hardware groups.

---

## 🖥️ Phase 5: Simulation & Visualization Module

### `server.py`
- **What it does:** The FastAPI webserver that hosts the frontend UI and pushes real-time WebSocket data.
- **Why we need it:** This serves the beautiful 3D dashboard you see in the browser.

### `playback_engine.py` / `scene_renderer.py`
- **What it does:** Acts like a virtual media player (Play, Pause, Seek). It schedules the Phase 4 instructions and manages the in-memory visual state of the stage over time.
- **Why we need it:** To simulate actual time passing on stage so the lights fade, switch, and transition smoothly.

### `color_utils.py` / `threejs_adapter.py`
- **What it does:** Translates words like "warm_amber" into hex colors (`#FFBF00`) and packages them perfectly for the Three.js 3D library on the frontend.
- **Why we need it:** A web browser doesn't know what "warm_amber" means; it mathematically needs hex codes and XYZ coordinates to render properly.

---

## 🛡️ Phase 6: Orchestration Module

### `__init__.py` / `cue_validator.py`
- **What it does:** Acts as the deterministic strict "Gate-keeper". It cross-checks all LLM generated cues against hard physical limits (e.g., confirming a fixture actually has a color wheel before sending it blue).
- **Why we need it:** AI hallucinates. This script mathematically ensures the generated logic is safe, preventing hardware crashes or impossible instructions from reaching the real stage.

---

## 📊 Phase 7: Evaluation Module

### `trace_logger.py` / `schemas.py`
- **What it does:** Silently records every logic decision, API call, and parameter shift the AI makes per scene into a `trace.json` file.
- **Why we need it:** If the lighting looks bad, we can read the trace log to debug exactly *why* the AI chose those colors.

### `metrics.py` (and `evaluation/` folder)
- **What it does:** The engine powering the "Evaluation Dashboard" (SCH, CFT, STB, etc...). It calculates mathematical scores for coherence, drift, and conflicts across the whole script.
- **Why we need it:** It provides humans with a single "PASS/WARN" grade so directors don't have to manually proof-read thousands of lines of generated JSON code.

---

## 🔌 Phase 8: Hardware/DMX Output (Placeholder)

### `__init__.py`
- **What it does:** An empty placeholder module meant for future implementation of Art-Net or serial DMX controllers.
- **Why we need it:** In the future, this is the file that will convert semantic intents (Intensity 80%) into raw DMX bytes (Value: 204) to control actual physical bulbs in a real auditorium.
