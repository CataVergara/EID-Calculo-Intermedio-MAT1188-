"""Comprueba la duración del guion y las escenas ejecutadas por Manim."""

import tempfile
import unittest

from manim import LEFT, RIGHT, Square, tempconfig

from scenes import escenas
from utils.guion import DURACION_TOTAL, GUION


class GuionTest(unittest.TestCase):
    def test_tiempos_de_las_tres_voces(self):
        self.assertAlmostEqual(DURACION_TOTAL, 315)
        for nombre, esperado in (("Catalina Vergara", 87.6),
                                 ("Ignacio De Celis", 128.4),
                                 ("Marcelo Santana", 99)):
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
                    self.assertIsNone(escena._resaltado)
                    with self.assertRaises(ValueError):
                        escena.esperar_hasta(duracion - 2)

    def test_recuadro_permanece_durante_la_pausa_y_cambia_con_el_foco(self):
        with tempfile.TemporaryDirectory() as directorio, tempconfig({
            "quality": "low_quality", "frame_rate": 60,
            "write_to_movie": False, "save_last_frame": False,
            "media_dir": directorio, "verbosity": "ERROR", "progress_bar": "none",
        }):
            escena = escenas.Portada(skip_animations=True)

            def comprobar():
                primero, segundo = Square().shift(LEFT * 2), Square().shift(RIGHT * 2)
                escena.add(primero, segundo)
                escena.resaltar(primero)
                recuadro = escena._resaltado
                escena.wait(2)
                self.assertIn(recuadro, escena.mobjects)
                escena.resaltar(segundo)
                self.assertNotIn(recuadro, escena.mobjects)
                self.assertIn(escena._resaltado, escena.mobjects)
                escena.quitar_resaltado()
                self.assertIsNone(escena._resaltado)
                escena.resaltar(primero)
                recuadro_final = escena._resaltado
                escena.finalizar()
                self.assertNotIn(recuadro_final, escena.mobjects)

            escena.construct = comprobar
            escena.render()
