"""Renderiza las escenas en orden narrativo y genera un MP4 con FFmpeg."""

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
SCENES = (
    "Portada", "TeoriaSigno", "TeoriaDefiniciones", "EjemploPrincipal",
    "Rectangulos", "SumaDeAportes", "Refinamiento", "ComparacionFinal",
    "RespuestaCentral", "Creditos",
)
QUALITY_DIRS = {
    "ql": "480p15", "qm": "720p30", "qh": "1080p60", "qk": "2160p60",
}


def concatenate(base, output):
    """Usa solo las diez escenas esperadas; nunca incluye un video final previo."""
    missing = [name for name in SCENES if not (base / f"{name}.mp4").is_file()]
    if missing:
        raise FileNotFoundError("Faltan escenas: " + ", ".join(missing))
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        from imageio_ffmpeg import get_ffmpeg_exe
        ffmpeg = get_ffmpeg_exe()
    if output.resolve() in [(base / f"{name}.mp4").resolve() for name in SCENES]:
        raise ValueError("La salida no puede sobrescribir una escena de entrada.")
    output.parent.mkdir(parents=True, exist_ok=True)
    playlist = base / "concat_list.txt"
    playlist.write_text("".join(f"file '{name}.mp4'\n" for name in SCENES), encoding="utf-8")
    subprocess.run(
        [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(playlist),
         "-c", "copy", "-movflags", "+faststart", str(output)],
        check=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quality", choices=QUALITY_DIRS, default="qh")
    parser.add_argument("--output", type=Path,
                        default=Path("media/output/MAT1188_EID_G06_2026.mp4"))
    parser.add_argument("--skip-render", action="store_true",
                        help="Unir las escenas ya renderizadas en la calidad elegida.")
    args = parser.parse_args()
    if not args.skip_render:
        subprocess.run(
            [sys.executable, "-m", "manim", "render", f"-{args.quality}",
             "scenes/escenas.py", *SCENES], cwd=ROOT, check=True,
        )
    base = ROOT / "media" / "videos" / "escenas" / QUALITY_DIRS[args.quality]
    output = args.output if args.output.is_absolute() else ROOT / args.output
    concatenate(base, output)
    print(f"Video generado: {output}")


if __name__ == "__main__":
    main()
