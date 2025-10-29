## 🧩 Modular Overlay System

The fullscreen overlay controls are now handled by a dedicated `FloatingOverlay` class located in `modules/overlay.py`. This module:

- Creates a floating control window with play/pause/stop buttons
- Tracks mouse movement to show/hide the overlay
- Integrates seamlessly with `PlaylistPlayer` via callbacks
- Automatically disables fullscreen for audio files

🎛️ Version: `v1.3.0` — Modular overlay and fullscreen refinement
