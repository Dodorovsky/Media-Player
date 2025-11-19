# DK_9000

A retro-inspired media player built with Python/Tkinter, born from the idea of DJ software and expanded through cinema.  
DK_9000 started as a simple audio project and evolved into a creative tool with playlists, radio streams, video playback, and compact UI modes.  
This is my first project developed with AI assistance: Copilot acted as a tutor, helping me push the code further than a basic tutorial.

## Motivation
DK_9000 started as a simple media player project — the foundation for any DJ software since it handles audio. Later, I decided to introduce video support, which was a real challenge, but as a cinema lover it became one of the most rewarding parts of the project.

## Learning Journey
I have been studying Python for about 3 years, with ups and downs.  
Courses such as [Píldoras Informáticas by Juan Díaz](https://www.pildorasinformaticas.es/) and [Cristian Koch’s Pygame course on Udemy](https://www.udemy.com/course/learn-python-by-making-games/) gave me the foundation to build DK_9000 without losing control of the project.

## Copilot as Instructor
This is my first project where I used AI assistance. Copilot acted as a tutor, guiding me through modularization, debugging, and expanding the player far beyond the initial tutorial.

## Features
- Audio and video playback with automatic detection
- Playlist management with duplicate control
- A five-band equalizer, expandable with a dedicated button
- Floating overlay with playback controls
- Visual feedback: time indicators shift from grey to green during playback
- Random and loop modes for flexible listening
- Fullscreen mode for video
- Compact mode: +/- button hides the listbox or video frame
- Hotkeys for quick control (e.g. Left: skip back, M: mute)
- Help button showing all key bindings

## Radio Stations
DK_9000 includes four curated radio streams, reflecting different moods and influences:
- NTS: electronic and experimental
- KEXP: indie rock and alternative
- SomaFM: jazzy and eclectic
- Classic FM: timeless classical repertoire

## Installation
Clone the repository and run the main script:
```bash
git clone https://github.com/yourusername/DK_9000.git
cd DK_9000
python main.py
```

Usage

· Load or create playlists in .txt format

· Add tracks without duplicates

· Expand the equalizer to adjust frequencies

· Switch to fullscreen for video playback

· Explore the radio stations for continuous streams

· Use compact mode and hotkeys for fast control

Project Structure

· ui.py → main interface

· playlist_manager.py → playlist logic

· overlay.py → floating overlay

· utils.py → helper functions

Philosophy / Design Notes

DK_9000 is not only a media player. It is an experiment in blending music, cinema, and software into a single retro-inspired artifact. The project was born from the idea that a simple player could serve as the foundation for DJ software, handling audio as its core. From there, video support was introduced — a challenge that reshaped the project but also opened a new dimension. Cinema has always been part of my inspiration, and bringing video into DK_9000 gave it a second life.

The design choices are guided by a balance between functionality and atmosphere:

· Compact and expandable interface, allowing the user to hide or reveal elements such as the playlist, video frame, or equalizer.

· Visual cues that respond to playback, with time indicators shifting color to signal activity.

· Integration of curated radio stations, chosen not for technical necessity but for the joy of listening and discovery.

· Hotkeys and a help panel, emphasizing immediacy and control, reminiscent of classic hardware.

Future ideas remain part of the philosophy. VU meters, once tested but removed due to technical issues, are envisioned as a possible return — glowing alongside the equalizer, adding a visual rhythm to the sound. DK_9000 is meant to evolve, shaped by both technical progress and aesthetic exploration.

In essence, DK_9000 is a personal journey: a project that began as a tutorial, grew through experimentation, and now stands as a creative tool. It is not intended to compete with professional media players such as VLC, but to exist as a unique intersection of code, sound, and vision.
