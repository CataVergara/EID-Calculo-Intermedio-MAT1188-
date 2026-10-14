"""Contrasta la suma numérica con integrales y puntos medios racionales exactos."""

from fractions import Fraction
import unittest

from scenes.escenas import fmt
from utils.comun import A_MAS, A_MENOS, AREA_TOTAL, INTEGRAL, sumas_punto_medio


def primitiva(x):
    return x**3 / 3 - 4 * x


class CalculosTest(unittest.TestCase):
    def test_regiones_exactas(self):
        a, r1, r2, b = map(Fraction, (-3, -2, 2, 3))
        positivo = primitiva(r1) - primitiva(a) + primitiva(b) - primitiva(r2)
        negativo = -(primitiva(r2) - primitiva(r1))
        self.assertEqual(positivo, Fraction(14, 3))
        self.assertEqual(negativo, Fraction(32, 3))
        self.assertAlmostEqual(A_MAS, float(positivo))
        self.assertAlmostEqual(A_MENOS, float(negativo))
        self.assertAlmostEqual(INTEGRAL, -6)
        self.assertAlmostEqual(AREA_TOTAL, float(Fraction(46, 3)))

    def test_sumatorias_con_puntos_racionales(self):
        for n in (6, 12, 24, 48):
            with self.subTest(n=n):
                dx = Fraction(6, n)
                aportes = [((-3 + (Fraction(i) + Fraction(1, 2)) * dx)**2 - 4) * dx
                           for i in range(n)]
                positivo = sum(x for x in aportes if x >= 0)
                negativo = sum(x for x in aportes if x < 0)
                esperado = (positivo, negativo, positivo + negativo, positivo - negativo)
                for resultado, exacto in zip(sumas_punto_medio(n), esperado):
                    self.assertAlmostEqual(resultado, float(exacto))

    def test_refinamiento_reduce_errores(self):
        error_integral = error_area = float("inf")
        for n in (6, 12, 24, 48):
            _, _, firmado, area = sumas_punto_medio(n)
            self.assertLess(abs(firmado - INTEGRAL), error_integral)
            self.assertLess(abs(area - AREA_TOTAL), error_area)
            error_integral, error_area = abs(firmado - INTEGRAL), abs(area - AREA_TOTAL)

    def test_n_invalido(self):
        for n in (0, -1, 2.5, True):
            with self.subTest(n=n), self.assertRaises(ValueError):
                sumas_punto_medio(n)

    def test_redondeo_en_tabla(self):
        self.assertEqual(fmt(sumas_punto_medio(12)[2]), "-6{,}13")
        self.assertEqual(fmt(sumas_punto_medio(24)[3]), "15{,}34")
