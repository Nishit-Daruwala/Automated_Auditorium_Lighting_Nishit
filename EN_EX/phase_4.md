# Phase 4: LLM Lighting Decision Engine

## Entry Points
- `phase_4/__init__.py` → Exposes the `LightingDecisionEngine` and convenience functions `generate_lighting_instruction` and `batch_generate_instructions` that map scene emotions to logical lighting groups.

## Exit Points
- `phase_4/lighting_decision_engine.py` → Returns `LightingInstruction` Pydantic models carrying semantic intents (color, intensity, focus area) designated for hardware groups (e.g., front_wash, side_fill). No DMX logic is generated here.

## Python Files Used

- `__init__.py`
  - **Role:** Main interface providing Phase 4 core engines and constant definitions.
  - **Functions / Classes:** Exports `LightingDecisionEngine`, `generate_lighting_instruction`, `batch_generate_instructions`, `LightingInstruction`, `GroupLightingInstruction`, etc.
  - **Connected Files:** `lighting_decision_engine.py`

- `lighting_decision_engine.py`
  - **Role:** Applies a RetrieverProtocol (Phase 3) context mapped with emotion outputs (Phase 2) to build prompt contexts. Pushes constraints to an LLM to receive semantic lighting parameters, falling back to rule-based algorithms upon API failure.
  - **Functions / Classes:** `RetrieverProtocol`, `SimpleRetriever`, `LightingDecisionEngine`, `LightingInstruction`, `GroupLightingInstruction`, `LightingParameters`, `TimeWindow`, `Transition`, `get_retriever`.
  - **Input Sources:** Dict objects describing a scene (text, timing, and emotion).
  - **Output Results:** `LightingInstruction` instances containing structured parameters for 5 critical stage lighting groups (`front_wash`, `back_light`, `side_fill`, `specials`, `ambient`).
  - **Connected Files:** Bridges logically between Phase 3 RAG and Phase 5 Stage/Playback engines.
