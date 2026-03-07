# Phase 1: Script Parsing and Scene Structure Processing

## Workflow
Phase 1 is the entry point of the Lumina Automated Lighting project. It focuses on safely acquiring, structuring, and breaking down a given script (PDF, TXT, or DOCX) into distinct, manageable scenes while resolving temporal constraints (timestamps).

1. **Text Acquisition (Phase 1A):** Reads raw text from the input document using Python libraries or OCR techniques as fallback.
2. **Immutable Structuring (Phase 1B):** Formats the text into an immutable data structure, breaking it into lines with cryptographic hashing to ensure the raw script's integrity is preserved throughout processing.
3. **Chunk Preprocessing:** Splits the script into LLM-friendly token chunks.
4. **Structural Intelligence (Phase 1C):** 
   - Uses an LLM (Large Language Model) to identify scene boundaries. 
   - Post-LLM, runs a deterministic boundary snapping algorithm that anchors the start/end lines to classical script markers (e.g., `INT.`, `EXT.`, `FADE IN`).
   - Uses a Hybrid Timestamp Assignment engine to determine explicit script timestamps and interpolate predictions for missing pacing durations.
5. **Deterministic Validation (Phase 1D):** Triggers a "Validation Layer" to catch hallucinatory boundary segmentations. If discrepancies exist, it falls back to a deterministic rule-based segmenter.
6. **Scene Output (Phase 1E):** Generates JSON output consisting of the final structured scenes and sequence metadata which moves downstream to Phase 2.

## How it Connects
Phase 1 produces a sequence of Scene Dictionary objects `[ {scene_id: "001", text: "...", start_time: X, end_time: Y}, ... ]`. This payload forms the baseline data source for the rest of the pipeline. Specifically, the clean text and scene boundaries are passed immediately to **Phase 2 (AI Emotion Analysis)** so that emotion detection only operates on well-defined narrative chunks rather than unstructured plaintext.
