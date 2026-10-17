"""Comprueba que la edición no trunque ni duplique tomas por error."""

import unittest

from utils.edicion import RECORTES, duracion_audio, validar_recortes
from utils.guion import GUION


class EdicionTest(unittest.TestCase):
    def test_tomas_caben_y_conservan_pausa_entre_voces(self):
        validar_recortes()
        for escena in RECORTES:
            self.assertLessEqual(duracion_audio(RECORTES[escena]), GUION[escena][0])
        for escena in ("TeoriaDefiniciones", "SumaDeAportes"):
            self.assertAlmostEqual(GUION[escena][0] - duracion_audio(RECORTES[escena]), 0.5)

    def test_rechaza_voz_que_se_truncaria(self):
        with self.assertRaisesRegex(ValueError, "excede"):
            validar_recortes({"Portada": ((0, 11),)})

    def test_rechaza_tomas_duplicadas_desordenadas_o_invalidas(self):
        for tramos in (((0, 3), (2, 4)), ((5, 6), (1, 2)), ((3, 2),), ((0, float("nan")),)):
            with self.subTest(tramos=tramos), self.assertRaises(ValueError):
                validar_recortes({"Portada": tramos})
