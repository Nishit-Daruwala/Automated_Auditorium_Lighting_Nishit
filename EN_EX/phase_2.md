# Phase 2: Emotion Analysis Module

## Entry Points
- `phase_2/__init__.py` → Exposes the `analyze_emotion` function. Accepts either a scene dictionary (new format) or a raw string (old format) for backward compatibility with downstream consumers like `pipeline_runner.py` or `main.py`.

## Exit Points
- `phase_2/__init__.py` → Returns a dictionary containing the emotion result (`primary_emotion`, `confidence`, `secondary_emotions`, `sentiment_score`, `theatrical_context`) mapped to BOTH the old format and the new format. This acts as the output for this phase, to be merged into the scene data.

## Python Files Used

- `__init__.py`
  - **Role:** Backward-compatible wrapper for the emotion analyzer.
  - **Functions / Classes:** `analyze_emotion`
  - **Input Sources:** Scene dict (`{"scene_id": "...", "text": "..."}`) or a raw string.
  - **Output Results:** Dictionary containing primary, secondary, and accent emotion predictions along with confidence mappings for backward compatibility.
  - **Connected Files:** `emotion_analyzer.py`

- `emotion_analyzer.py`
  - **Role:** Stateless scene-local emotion classifier. Core engine that utilizes Llama 3.1 8B via HF APIs and DistilRoBERTa as a fallback.
  - **Functions / Classes:** `EmotionAnalyzer`, `EmotionAnalyzer.analyze`, `EmotionAnalyzer._run_llm`, `EmotionAnalyzer._run_classifier`, `EmotionAnalyzer._validate_output`, `get_analyzer`, `analyze_emotion`.
  - **Input Sources:** A scene dictionary payload containing text.
  - **Output Results:** A scene dictionary returned with a newly appended `emotion` section (primary, secondary, accent emotions & confidences) conforming to strict JSON structures.
  - **Connected Files:** Externally interfaces with Llama 3.1 via Hugging Face Inference API and DistilRoBERTa.
