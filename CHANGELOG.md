# 📓 CHANGELOG

## [2025-11-18] UI Feedback Sync — Small fixes, big harmony

– Play button no longer changes state if nothing is loaded.  
– Mute button resets to its original color when the volume slider is moved above 0.  
– Radio buttons now sync visually: all change color when radio is active, and the currently playing station is highlighted.  
– Playlist button now reflects playback state correctly.  
– Improved state detection: radio, playlist, and audio playback now trigger accurate color feedback.  
– Various subtle refinements from the past couple of days to stabilize and polish the interface.

🌀 DK_9000 responds with elegance. Everything is in its place.

---


This file documents significant changes made to the project.

## [v1.6.0] – 2025-11-15
### 🎙️ Sonic Stability & Visual Balance
- Full UI layout restored and stabilized across all media modes
- CRT and AMP effects finely tuned for cohesive retro visuals
- HAL indicator and list labels centered and visually aligned
- High-quality radio streams integrated with excellent performance
- Layout logic hardened for fullscreen transitions and media switching


---

## [2025-11-04] - VU Meter Layout Fix

### Fixed
- A visual gap was appearing between the VU meter and the label below.
- The `Canvas` height was set to `110px`, but the rectangles only reached `y=100`, leaving 10px unused.
- Adjusted the `Canvas` height to `100px` to eliminate the bottom gap.
- Result: the VU meter now appears aligned and compact, with no visual interference.

