# Phase 6: Orchestration & Control

## Workflow
Phase 6 manages pipeline execution, sequencing, and ensuring the Cues created in Phase 4 are perfectly timed, valid, and batched for the user or the hardware.

1. **Cue Validation (`cue_validator.py`):** Acts as a safety net. It validates the output `LightingInstruction` arrays from the generated JSON against strict rule logic.
   - Example Check: If a "snap" transition is paired with a slow 10-second fade duration, Phase 6 catches the contradiction.
   - Example Check: Ensures no invalid RGB values (>255) enter the visualization code.
2. **Cue Sheet Construction:** Batches all individualized scene cues into a master orchestration file (the "Cue Sheet"). 

## How it Connects
This phase intercepts the raw data from **Phase 4 (Lighting Decision)** before it reaches **Phase 5 (Visualization)** or the frontend UI. It is the final QA step.
