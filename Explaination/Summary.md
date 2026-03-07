# Pipeline Summary: Automated Lighting Sequence

The **Automated Auditorium Lighting System** is built on a highly modular 7-phase architecture. Its overarching goal is to transform a standard text document (a script, screenplay, or play format) into a fully actionable, time-coded metadata sequence of lighting hardware instructions—without requiring a human designer to manually plot out every mood and color shift.

## Architectural Flow
The pipeline moves linearly from unstructured text to physical (or simulated) execution.

### Stage 1: Ingestion & Structuring
1. **Phase 1 (Script Processing):** The raw script `.pdf`, `.docx`, or `.txt` arrives. Phase 1 handles formatting, cleaning, and slicing the text into structural "Scenes" (often demarcated by INT/EXT or blanks). It also assigns rough timestamps or absolute chronological duration for each scene. **(Output: Cleaned Scene Data + Timestamps)**

### Stage 2: Intelligence & Meaning
2. **Phase 2 (Emotion Analysis):** The clean scenes are fed into an LLM (Large Language Model) one-by-one alongside a global plot summary. The AI infers the deep emotional tone, narrative arc (e.g., Climax, Rising Action), and the exact feeling the scene is trying to evoke. **(Output: Emotional Vectors + Metadata)**
3. **Phase 3 (Knowledge Layer):** Using a Vector Database (RAG), the system cross-references the emotions found in Phase 2 with a specialized knowledge base defining how professional lighting designers light those emotions. **(Output: Lighting Strategy Bias)**

### Stage 3: Translation & Instruction
4. **Phase 4 (Lighting Decision):** Armed with precise feelings (Phase 2) and best-practice rules (Phase 3), the system generates rigid, formatted JSON containing actual lighting parameters (Intensity, Color Hex Codes, Fade durations, Groups like 'Wash', 'Spot'). **(Output: Semantic Lighting Instructions)**

### Stage 4: Safety & Execution
5. **Phase 6 (Orchestration):** The semantic lighting instructions are validated against constraint rules (e.g., catching impossible fade times or broken colors) and stitched into a Master Cue Sheet. **(Output: Validated Master Cue Sheet)**
6. **Phase 5 (Visualization):** The executed Master Cue Sheet is fed into the front-end (typically a 3D WebGL/Three.js render engine or DMX translator) to physically display the lights. **(Output: Visual Output / DMX)**
7. **Phase 7 (Evaluation):** Running passively in the background, this phase logs metrics on the lighting decisions to ensure the AI's choices were stable, consistent, and creatively accurate over long script durations.

## Conclusion
Each phase acts as an independent micro-service. **Phase 1** tells the system *when* things happen and what the characters say. **Phase 2** tells the system *how* they feel. **Phase 3 and 4** determine *what* the lights should exactly do about it. **Phases 6 and 5** make sure it happens safely and beautifully on stage, and **Phase 7** grades the performance.
