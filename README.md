# 🎭 Automated Auditorium Lighting System

**Lumina Intelligence** is an AI-driven, Human-in-the-Loop system that ingests theater scripts, understands scene-by-scene emotions, and automatically generates real-time, professional auditorium lighting designs mapped to physical stage hardware.

## ✨ Core Features
- 📚 **Multi-Format Parsing:** Support for `.txt`, `.pdf`, and `.docx` theater scripts.
- � **Emotional Intelligence:** Understands scene sentiment and pacing using Llama 3 Instruct & DistilRoBERTa.
- 🏛️ **Dual RAG Architecture:** Uses FAISS vector databases to anchor AI hallucinations strictly to real-world theatrical textbooks and physical hardware limits.
- ⏱️ **Timestamp Prediction:** Automatically calculates execution timelines based on script density.
- 🖥️ **Real-Time 3D Visualization:** Includes a FastAPI + Three.js web dashboard to visually preview lighting transitions.
- � **8-Check Evaluation Dashboard:** Mathematically scores the AI's logic (Conflicts, Drift, Stability) before stage execution.

---

## 🏗️ Project Architecture (The 8 Phases)

The project is structured into 8 modular phases:

1. **Phase 1: Script Parsing & Structuring** - Fragments scripts into logical, timestamped scenes.
2. **Phase 2: Emotion Analysis** - Identifies primary and secondary moods (e.g., joy, tension).
3. **Phase 3: Knowledge Layer (RAG)** - Retrieves professional lighting rules and limits from databases.
4. **Phase 4: LLM Lighting Decision Engine** - Formulates semantic lighting intents (Color, Intensity, Target).
5. **Phase 5: Simulation & Visualization** - Plays the cues in real-time on a 3D Web UI.
6. **Phase 6: Orchestration Validation** - Gatekeeps output against impossible hardware instructions.
7. **Phase 7: Evaluation Engine** - Scores coherence, drift, and conflicts (producing a WARN/PASS metric).
8. **Phase 8: Hardware Export (Future)** - Outgoing DMX512/Art-Net translations for actual stage dimmers.

*For rigorous details on every file, please see the `Explaination/File_understanding.md` and `Explaination/Other_Folder.md` documents.*

---

## 🚀 Installation & Setup

```bash
# 1. Clone the repository
git clone <repository-url>
cd Automated_Auditorium_Lighting

# 2. Setup Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Dependencies
pip install -r requirements.txt
```

---

## 🕹️ Quick Start Guide

### 1. Generating Lighting Cues from a Script (Backend)
Process a raw script (TXT/PDF/DOCX) through the pipeline to generate standardized JSON output:
```bash
python main.py data/raw_scripts/sample_play.txt
```

Translate the Phase 1 parsed scenes directly into semantic lighting cues (Phase 2/4):
```bash
python main_phase2.py data/standardized_output/sample_play_processed.json
```

### 2. Running the 3D Visualizer (Frontend)
Host the FastAPI server to preview generated cues in your web browser:
```bash
python app.py
```
*Navigate to `http://localhost:8000` in your browser to view the realtime 3D simulation.*

### 3. Running Diagnostics
Verify that your local environment has the required models, folders, and API keys:
```bash
python run_diagnostics.py
```

---

## ⚙️ Configuration

System thresholds, timeout flags, LLM models, and default file paths can be tuned by editing the master `config.py` file.

- `OLLAMA_ENABLED`: Toggle local AI evaluation vs Cloud.
- `WORDS_PER_MINUTE`: Modifies automatic timestamp estimation speeds.
- `USE_VECTOR_DB`: Toggle the FAISS retrieval engine.

---

## 📁 Data Structure
- `data/raw_scripts/`: Place your input scripts here.
- `data/standardized_output/`: The parsed JSON equivalents of your scripts.
- `data/lighting_cues/`: The final AI-generated lighting sequences.
- `data/traces/`: JSON logging footprints recorded by the Evaluation engine for math analysis.

---

## 🛡️ Support & Documentation
Comprehensive presentation materials and explanations can be found in the `Explaination/` folder:
- **`Q_A.md`** - Common project questions and answers.
- **`File_understanding.md`** - A 4-line overview of every single python script.
- **`Light_Overview.md`** - Metric breakdowns of the Evaluation Dashboard.

## License
MIT