# 📓 CHANGELOG

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

