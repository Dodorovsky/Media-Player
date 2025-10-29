# 🎛️ 1979_MODEL ___ media_player >> by DODOROVSKY

A modular, retro-styled media player built with Tkinter and VLC. Inspired by vintage consoles and creative autonomy, this player blends functionality with visual storytelling. Every button, overlay, and layout choice reflects a modular mindset and a retro aesthetic.

---

## ✨ Features

- 📂 Playlist loading with drag-and-drop support
- 🎥 Video playback with embedded fullscreen mode
- 🎧 Audio-aware fullscreen guard
- 🛰️ Floating overlay controls (modularized in `modules/overlay.py`)
- 🔁 Loop and shuffle playback
- 🎚️ Volume control with retro meter
- 🧠 Smart layout restoration and fullscreen toggling
- 🧹 Clean UI separation via `setup_ui()` and modular callbacks

---

## 🧠 Design Philosophy

This media player is more than a tool — it's a creative artifact. Built by DODOROVSKY as part of a larger vision for a future DJ/media toolkit, it treats every feature as part of a narrative. From floating overlays to backup routines, each element reflects the artistic identity of the developer.

Modularity is key: logic is separated into reusable components, visual elements are styled with intention, and the codebase is structured to evolve with new ideas.

---

## 🚀 Getting Started

Install dependencies:

```bash
pip install python-vlc pillow tkinterdnd2

```

🛠️ Dependencies
python-vlc — VLC bindings for Python

Pillow — image handling for button graphics

tkinterdnd2 — drag-and-drop support

tkinter — core GUI framework (built-in with Python)

VLC — must be installed on your system

---

## 📁 Folder Structure

media_player/
├── graphics/
│   └── buttons_control/
├── modules/
│   └── overlay.py
├── player.py
├── ui2.py
├── utils.py

---

## 📘 Version History

· v1.3.0 — Modular overlay system, fullscreen logic refined

· v1.2.0 — Stable fullscreen + overlay guard

· v0.9-alpha — Initial UI layout and playback working

---

## 🧩 Modular Overlay System
The fullscreen overlay controls are now handled by a dedicated FloatingOverlay class located in modules/overlay.py. This module:

· Creates a floating control window with play/pause/stop buttons

· Tracks mouse movement to show/hide the overlay

· Integrates seamlessly with PlaylistPlayer via callbacks

· Automatically disables fullscreen for audio files

---

🎛️ Version: v1.3.0 — Modular overlay and fullscreen refinement

---

## 🧪 Creative Notes

Future ideas include:

🎛️ Modular control panels for DJ-style mixing

🧠 Narrative-driven backup and recovery routines

🖼️ Retro visual themes and animated overlays

🧩 Plugin system for custom media effects

This project is part of a larger creative ecosystem where software becomes stagecraft.

---

## Made with 🧠 and 🎛️ by DODOROVSKY


