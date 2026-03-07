# Phase 1: Script & Scene Structure Processing

## Entry Points
- `phase_1/__init__.py` → Orchestrates the entire Phase 1 pipeline via the `run_phase_1` function. This is the main entry point that receives a script path.

## Exit Points
- `phase_1/__init__.py` → Ultimately returns a tuple `(scenes, metadata)` containing schema-valid scene JSONs and metadata. (Generated via `phase_1/scene_json_builder.py`). This output will act as the trigger for succeeding phases.

## Python Files Used

- `__init__.py`
  - **Role:** Main orchestrator for Phase 1.
  - **Functions / Classes:** `run_phase_1`, `_snap_boundaries_to_markers`.
  - **Input Sources:** Script file path.
  - **Output Results:** Generated scene JSONs and metadata.
  - **Connected Files:** `text_acquisition.py`, `immutable_structurer.py`, `chunk_preprocessor.py`, `llm_scene_segmenter.py`, `timestamp_engine.py`, `validation_layer.py`, `scene_json_builder.py`, `compat.py`.

- `text_acquisition.py`
  - **Role:** Phase 1A — Text Acquisition (Direct or OCR).
  - **Functions / Classes:** `AcquisitionResult`, `acquire_text`.
  - **Input Sources:** Script file path.
  - **Output Results:** `AcquisitionResult` containing text and provenance metadata.

- `immutable_structurer.py`
  - **Role:** Phase 1B — Immutable Structuring. Creates frozen, auditable coordinate systems for the text.
  - **Functions / Classes:** `ImmutableText`, `structure_text`.
  - **Input Sources:** Acquired raw text from `text_acquisition.py`.
  - **Output Results:** `ImmutableText` object instance.

- `chunk_preprocessor.py`
  - **Role:** Splits the immutable text into overlapping structural chunks for LLM processing.
  - **Functions / Classes:** `ChunkInfo`, `create_chunks`.
  - **Input Sources:** `ImmutableText`.
  - **Output Results:** List of `ChunkInfo` objects.

- `llm_scene_segmenter.py`
  - **Role:** Phase 1C Call 1 — LLM Scene Segmentation. Uses HuggingFace API/local models or rule-based fallbacks to segment scenes.
  - **Functions / Classes:** `segment_scenes_llm`, `segment_scenes_rulebased`.
  - **Input Sources:** List of `ChunkInfo` objects, `ImmutableText`.
  - **Output Results:** List of scene dictionaries containing line ranges.

- `timestamp_engine.py`
  - **Role:** Phase 1C Call 2 — Timestamp extraction and hybrid assignment to scenes.
  - **Functions / Classes:** `assign_timestamps`.
  - **Input Sources:** List of LLM-segmented scenes, `ImmutableText`.
  - **Output Results:** Enriched scenes with start and end times, durations, and confidence details.

- `validation_layer.py`
  - **Role:** Phase 1D — Deterministic Validation & Fallback. Ensures segmented scenes contain no overlaps and conform to structural rules before building output.
  - **Functions / Classes:** `validate_and_enforce`.
  - **Input Sources:** Segmented scenes with timestamps, `ImmutableText`.
  - **Output Results:** Validated scenes and a `ValidationResult`.

- `scene_json_builder.py`
  - **Role:** Phase 1E — Formats internal data models into final schema-conformant JSON representations.
  - **Functions / Classes:** `build_scene_json`, `build_phase1_metadata`.
  - **Input Sources:** Validated scenes and `ImmutableText`.
  - **Output Results:** Final project scene representations conforming to `contracts/scene_schema.json`.

- `compat.py`
  - **Role:** Backward compatibility for old API structures. Re-exports functions to not break integrations that used an older variant.
