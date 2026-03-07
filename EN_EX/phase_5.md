# Phase 5: Simulation & Visualization Module

## Entry Points
- `phase_5/server.py` → FastAPI application serving as the integration point between backend playback and frontend visualization. Bootstraps the `PlaybackEngine` and listens for playback control commands over WebSockets (`/ws`).
- `phase_5/playback_engine.py` → The `PlaybackEngine.load_instructions` function serves as the programmatic entry point to load `LightingInstruction` generated from Phase 4.

## Exit Points
- `phase_5/server.py` → Pushes real-time visual states (encoded as JSON) over the WebSocket `/ws` connection to the connected frontend client.
- `phase_5/threejs_adapter.py` → Translates abstract light states into a concrete JSON structure containing 3D coordinates and parameters ready for Three.js rendering.

## Python Files Used

- `__init__.py`
  - **Role:** Exposes components for Phase 5.
  - **Connected Files:** `color_utils.py`, `playback_engine.py`.

- `playback_engine.py`
  - **Role:** Orchestrates the timing, transitions, and execution of `LightingInstruction` sets over time. Includes methods like `play`, `pause`, `stop`, `seek`, and `update`.
  - **Functions / Classes:** `PlaybackEngine`.
  - **Input Sources:** Schema-valid lists of `LightingInstruction` dictionaries.
  - **Output Results:** Periodically updates the `SceneRenderer` with actively processed visual states.

- `scene_renderer.py`
  - **Role:** Maintains the in-memory visual representation and state of the active auditorium lights.
  - **Functions / Classes:** `LightState`, `SceneRenderer`.
  - **Input Sources:** Instruction updates triggered by `PlaybackEngine`.
  - **Output Results:** Exposes the current lighting state via `get_all_states()`.

- `color_utils.py`
  - **Role:** Helper utility responsible for color conversions, translating semantic colors (e.g., `"warm_amber"`) to hex values.
  - **Functions / Classes:** `rgb_to_hex`, `get_color_name`, `dmx_to_percent`, `get_intensity_label`, `get_hex_from_semantic`.

- `threejs_adapter.py`
  - **Role:** Acts as a bridge, adapting raw renderer states into a format containing XYZ placement, intensities, and colors usable by a Three.js web client.
  - **Functions / Classes:** `ThreeJSAdapter`.
  - **Input Sources:** Raw states from `SceneRenderer`.
  - **Output Results:** Dictionary representing frame packets with timestamp and corresponding `lights` data.

- `server.py`
  - **Role:** Web server handling web socket communication and broadcasting 3D-mapped lighting structures derived from `ThreeJSAdapter`.
  - **Functions / Classes:** `get` (HTML endpoint), `websocket_endpoint`.
  - **Input Sources:** Incoming WebSocket requests ("play", "pause", "stop").
  - **Output Results:** JSON packets over WebSockets containing {"status", "visuals"}.
