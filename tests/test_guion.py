"""Comprueba la duración del guion y las escenas ejecutadas por Manim."""

import tempfile
import unittest

from manim import tempconfig

from scenes import escenas
from utils.guion import DURACION_TOTAL, GUION


class GuionTest(unittest.TestCase):
    def test_tiempos_de_voces_y_bloque_pendiente(self):
        self.assertAlmostEqual(DURACION_TOTAL, 321)
        for nombre, esperado in (("Catalina Vergara", 87.6),
                                 ("Ignacio De Celis", 128.4),
                                 ("Marcelo Santana", 105)):
            with self.subTest(voz=nombre):
                self.assertAlmostEqual(sum(d for d, voz in GUION.values() if voz == nombre), esperado)

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
