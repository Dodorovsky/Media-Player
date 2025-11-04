# 📓 CHANGELOG

This file documents significant changes made to the project.

---

## [2025-11-04] - VU Meter Layout Fix

### Fixed
- A visual gap was appearing between the VU meter and the label below.
- The `Canvas` height was set to `110px`, but the rectangles only reached `y=100`, leaving 10px unused.
- Adjusted the `Canvas` height to `100px` to eliminate the bottom gap.
- Result: the VU meter now appears aligned and compact, with no visual interference.

