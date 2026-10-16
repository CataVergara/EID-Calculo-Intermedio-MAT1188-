"""Comprueba la duración del guion y las escenas ejecutadas por Manim."""

import tempfile
import unittest

from manim import tempconfig

from scenes import escenas
from utils.guion import DURACION_TOTAL, GUION


class GuionTest(unittest.TestCase):
    def test_cinco_minutos_quince_y_tres_bloques_iguales(self):
        self.assertEqual(DURACION_TOTAL, 315)
        for nombre in ("Catalina Vergara", "Ignacio De Celis", "Marcelo Santana"):
            with self.subTest(voz=nombre):
                self.assertEqual(sum(d for d, voz in GUION.values() if voz == nombre), 105)

    def test_escenas_completan_su_tiempo_sin_superponer_textos(self):
        with tempfile.TemporaryDirectory() as directorio, tempconfig({
            "quality": "low_quality", "frame_rate": 60,
            "write_to_movie": False, "save_last_frame": False,
            "media_dir": directorio, "verbosity": "ERROR", "progress_bar": "none",
        }):
            for nombre, (duracion, _) in GUION.items():
                with self.subTest(escena=nombre):
                    escena = getattr(escenas, nombre)(skip_animations=True)
                    escena.render()
                    self.assertAlmostEqual(escena.time, duracion, delta=1 / 60 + 0.001)
                    self.assertFalse(getattr(escena, "_avisos", set()))
                    with self.assertRaises(ValueError):
                        escena.esperar_hasta(duracion - 2)
