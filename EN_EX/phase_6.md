# Phase 6: Orchestration Module

## Entry Points
- `phase_6/__init__.py` → Exposes cue validation tools (`validate_cue`, `validate_cue_sheet`) that gatekeep generated lighting cues before execution.

## Exit Points
- `phase_6/cue_validator.py` → Returns a validation tuple `(is_valid: bool, errors: List[str], warnings: List[str])`. Valid configurations proceed, while errors block execution and trigger fallbacks or notifications.

## Python Files Used

- `__init__.py`
  - **Role:** Main interface for the Phase 6 Orchestration module.
  - **Functions / Classes:** Exports `validate_cue`, `validate_cue_sheet`.
  - **Connected Files:** `cue_validator.py`.

- `cue_validator.py`
  - **Role:** Provides deterministic structural check of physical light targets and DMX boundaries against the fixture capabilities extracted from Phase 3 Knowledge Layers.
  - **Functions / Classes:** `CueValidator`, `CueValidator.validate_cue`, `validate_cues`.
  - **Input Sources:** A generated `cue_data` dictionary and external queries to the `pipeline.rag_retriever` to fetch physical fixture limits (DMX bounds, valid parameters).
  - **Output Results:** Tuple asserting boolean validity and accompanied by text arrays for errors and warnings.
