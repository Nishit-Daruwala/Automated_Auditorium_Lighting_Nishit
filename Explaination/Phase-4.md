# Phase 4: LLM Lighting Decision Engine

## Workflow
Phase 4 converts the emotional context and metadata into concrete, stage-ready lighting parameters without relying on raw DMX signals directly. This allows the backend to be software and hardware agnostic.

1. **Intake Variables:** Receives the Scene ID, the primary emotion ("Tension"), transition type, confidence scores from Phase 2, and the RAG-inspired best practices from Phase 3.
2. **LLM Translation Layer:** Uses the LLM to generate targeted Lighting Instructions. 
3. **Pydantic Validation (LightingInstruction):**
   - The LLM constructs sub-groups (`GroupLightingInstruction`) such as `Wash`, `Spot`, `Effect`, or `House`.
   - Each group contains exact parameters: `intensity` (0-100), `color_temp`, `rgb` arrays, `pan/tilt` instructions, and `focus` logic (e.g., center stage, wide, stage left).
4. **Transition Generation:** Defines transition dynamics, like Fade-In, Snap, Crossfade, along with required duration.

## How it Connects
Phase 4 transforms theoretical logic (Feelings and Timing) from **Phase 2** into Mechanical Instructions (Intensity, Position, Color, Transition). It exports standard JSON architectures representing lighting Cues that are fully readable by external visualizers or orchestration software in **Phase 5 and Phase 6**.
