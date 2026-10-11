"""Comprueba el contrato de ensamblado sin ejecutar Manim ni FFmpeg."""

from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from render import SCENES, concatenate


class RenderTest(unittest.TestCase):
    def test_orden_y_exclusion_de_resultados_anteriores(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            for name in SCENES:
                (base / f"{name}.mp4").touch()
            (base / "VIDEO_FINAL.mp4").touch()
            output = base / "salida con espacios" / "nuevo.mp4"
            with patch("render.shutil.which", return_value="ffmpeg"), patch("render.subprocess.run") as run:
                concatenate(base, output)
            self.assertEqual((base / "concat_list.txt").read_text().splitlines(),
                             [f"file '{name}.mp4'" for name in SCENES])
            self.assertEqual(SCENES[0], "Portada")
            self.assertEqual(SCENES[-1], "Creditos")
            self.assertTrue(output.parent.is_dir())
            self.assertTrue(run.call_args.kwargs["check"])
            self.assertEqual(run.call_args.args[0][-1], str(output))

    def test_falta_una_escena(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            with patch("render.subprocess.run") as run, self.assertRaises(FileNotFoundError):
                concatenate(base, base / "nuevo.mp4")
            run.assert_not_called()

    def test_fallo_de_ffmpeg_se_propaga(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            for name in SCENES:
                (base / f"{name}.mp4").touch()
            with patch("render.shutil.which", return_value="ffmpeg"), patch(
                "render.subprocess.run", side_effect=subprocess.CalledProcessError(1, "ffmpeg")
            ), self.assertRaises(subprocess.CalledProcessError):
                concatenate(base, base / "nuevo.mp4")

    def test_no_sobrescribe_una_escena(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            for name in SCENES:
                (base / f"{name}.mp4").touch()
            with patch("render.shutil.which", return_value="ffmpeg"), self.assertRaises(ValueError):
                concatenate(base, base / "Portada.mp4")
