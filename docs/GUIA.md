# Guía rápida

- `scenes/escenas.py`: las diez escenas del video.
- `utils/comun.py`: cálculos, colores y constructores visuales.
- `render.py`: render y ensamblado en orden narrativo, para macOS/Linux/Windows.
- `render.ps1`: acceso al mismo flujo desde PowerShell.
- `media/output/`: videos generados, ignorados por Git.
- `tests/`: verificación de cálculos y ensamblado.

Desde la raíz, con el entorno virtual activo: `python render.py --quality ql`.
Para 1080p60: `python render.py --quality qh`.
La instalación y los comandos completos están en [README](../README.md).
