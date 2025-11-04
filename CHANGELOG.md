# 📓 CHANGELOG

Este archivo documenta los cambios significativos realizados en el proyecto.

---

## [2025-11-04] - VU Meter Layout Fix

### Fixed
- Se observaba un espacio visual entre el VU meter y la etiqueta inferior.
- El `Canvas` tenía altura de `110px`, pero los rectángulos solo llegaban hasta `y=100`, dejando 10px sin contenido.
- Se ajustó la altura del `Canvas` a `100px` para eliminar el espacio inferior.
- Resultado: el VU meter ahora se ve alineado y compacto, sin interferencias visuales.
