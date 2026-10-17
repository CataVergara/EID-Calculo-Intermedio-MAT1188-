"""Comprueba que la edición no trunque ni duplique tomas por error."""

import unittest

from utils.edicion import RECORTES, duracion_editada, insertar_pcm, validar_recortes
from utils.guion import GUION


class EdicionTest(unittest.TestCase):
    def test_tomas_caben_y_conservan_pausa_entre_voces(self):
        validar_recortes()
        for escena in RECORTES:
            self.assertLessEqual(duracion_editada(escena, RECORTES[escena]), GUION[escena][0])
        self.assertAlmostEqual(duracion_editada("TeoriaDefiniciones", RECORTES["TeoriaDefiniciones"]), 40.44)
        self.assertAlmostEqual(GUION["SumaDeAportes"][0] - duracion_editada("SumaDeAportes", RECORTES["SumaDeAportes"]), 0.5)

    def test_insertos_conservan_el_audio_y_las_posiciones_originales(self):
        # Dos frames por segundo y dos bytes por frame, como un PCM mono de 16 bits.
        original = b"aabbccdd"
        self.assertEqual(insertar_pcm(original, [(0.5, b"00"), (1.5, b"ee")], 2, 2),
                         b"aa00bbcceedd")
        for insertos in ([(3, b"ee")], [(1, b"e")], [(1.5, b"ee"), (0.5, b"ee")]):
            with self.subTest(insertos=insertos), self.assertRaises(ValueError):
                insertar_pcm(original, insertos, 2, 2)

    def test_rechaza_voz_que_se_truncaria(self):
        with self.assertRaisesRegex(ValueError, "excede"):
            validar_recortes({"Portada": ((0, 11),)})

    def test_rechaza_tomas_duplicadas_desordenadas_o_invalidas(self):
        for tramos in (((0, 3), (2, 4)), ((5, 6), (1, 2)), ((3, 2),), ((0, float("nan")),)):
            with self.subTest(tramos=tramos), self.assertRaises(ValueError):
                validar_recortes({"Portada": tramos})
