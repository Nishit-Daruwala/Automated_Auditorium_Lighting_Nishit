# Phase 7: Evaluation Module

## Entry Points
- `phase_7/trace_logger.py` → Exposes the `TraceLogger` class, specifically the `log_decision` method, which is the main entry point for tracking scene-by-scene pipeline transformations.
- `phase_7/metrics.py` → Exposes the `MetricsEngine` class, specifically the `generate_report` method, which serves as the entry point for running post-generation evaluations based on saved instructions.

## Exit Points
- `phase_7/trace_logger.py` → Uses the `save` method to build and export a JSON artifact (e.g. `data/traces/trace_xxxxx.json`) capturing the full execution trace.
- `phase_7/metrics.py` → Returns a computation dictionary carrying research-grade metrics (e.g., coverage, parameter diversity, drift, determinism).

## Python Files Used

- `__init__.py`
  - **Role:** Empty placeholder initialization for the Phase 7 evaluation module.

- `trace_logger.py`
  - **Role:** Logs input/output traces per scene for reproducibility and offline assessment.
  - **Functions / Classes:** `TraceLogger`, `TraceLogger.log_decision`, `TraceLogger.save`.
  - **Input Sources:** Dict objects describing a scene and the correspondingly generated Phase 4 instruction outputs.
  - **Output Results:** Saved `.json` files in the `data/traces/` directory mapping text hashes to executed traits.
  - **Connected Files:** Relies on `schemas.py` for structured representation.

- `schemas.py`
  - **Role:** Pydantic / Dataclass models validating the shape of logging payloads.
  - **Functions / Classes:** `RAGContextRef`, `TraceEntry`, `TraceLog`.

- `metrics.py`
  - **Role:** Central computation component invoking calculations on generated lighting parameters (coverage, drift).
  - **Functions / Classes:** `MetricsEngine`, `MetricsEngine.generate_report`.
  - **Input Sources:** A list of parsed lighting instructions (Phase 4 objects).
  - **Output Results:** Generates a summary evaluation report dictionary.
  - **Connected Files:** Invokes logic residing in `evaluation/coverage.py`, `evaluation/consistency.py`, and `evaluation/stability.py`.

- `evaluation/coverage.py`, `evaluation/consistency.py`, `evaluation/stability.py`
  - **Role:** Component math files handling the localized complexity of Jaccard similarity, transition diversity, and parameter drift calculations required by `MetricsEngine`.
