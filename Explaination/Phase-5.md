# Phase 5: Visualization & Simulation Module

## Workflow
Phase 5 is the rendering and visual execution step. It simulates the theoretical lighting decisions formulated in Phase 4 in a real-time 3D environment or prepares them for hardware playback.

1. **Color Utilities:** Processes the RGB values/Color Temp into render-friendly hex codes or specific gel types.
2. **Playback Engine Orchestration:** Manages the logical transition timings.
   - It reads the `duration` of the scene (from Phase 1).
   - It reads the `transition_type` and `transition_duration` (from Phase 4).
   - It outputs smooth interpolated values for a visualizer (like the Three.js web frontend) to consume.
3. **Execution Ready Data:** The final JSON produced by the backend includes exact instructions per fixture/group, structured for front-end rendering or physical DMX controllers.

## How it Connects
Phase 5 acts as the "Player." It transforms the static lighting cues defined in **Phase 4** and combines them with the timeline generated in **Phase 1** to create an animated, viewable lighting sequence in the browser UI.
