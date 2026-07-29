"""Pruebas del análisis de conjuntos definidos por ax + by = c."""

import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from analisis_vectorial import AnalisadorVectorial


class TestAnalisisSubespacios(unittest.TestCase):
    def test_recta_afin_x_mas_y_igual_10_no_es_subespacio(self):
        resultado = AnalisadorVectorial.analizar_subespacio_ecuacion(1, 1, 10)

        self.assertFalse(resultado.es_subespacio)
        self.assertFalse(resultado.contiene_cero)
        self.assertFalse(resultado.cierre_suma)
        self.assertFalse(resultado.cierre_escalar)
        self.assertIsNone(resultado.dimension)
        self.assertEqual(resultado.base.shape, (0, 2))
        self.assertTrue(any("(10, 0)" in paso for paso in resultado.calculos))
        self.assertTrue(any("(20, 0)" in paso for paso in resultado.calculos))

    def test_recta_homogenea_es_subespacio_de_dimension_uno(self):
        resultado = AnalisadorVectorial.analizar_subespacio_ecuacion(2, -4, 0)

        self.assertTrue(resultado.es_subespacio)
        self.assertTrue(resultado.contiene_cero)
        self.assertTrue(resultado.cierre_suma)
        self.assertTrue(resultado.cierre_escalar)
        self.assertEqual(resultado.dimension, 1)
        self.assertEqual(resultado.base.shape, (1, 2))
        np.testing.assert_allclose(
            np.array([2.0, -4.0]) @ resultado.base[0],
            0.0,
            atol=1e-9,
        )

    def test_ecuacion_nula_representa_todo_r2(self):
        resultado = AnalisadorVectorial.analizar_subespacio_ecuacion(0, 0, 0)

        self.assertTrue(resultado.es_subespacio)
        self.assertEqual(resultado.dimension, 2)
        np.testing.assert_array_equal(resultado.base, np.eye(2))

    def test_ecuacion_incompatible_representa_conjunto_vacio(self):
        resultado = AnalisadorVectorial.analizar_subespacio_ecuacion(0, 0, 1)

        self.assertFalse(resultado.es_subespacio)
        self.assertFalse(resultado.contiene_cero)
        self.assertIsNone(resultado.cierre_suma)
        self.assertIsNone(resultado.cierre_escalar)
        self.assertIsNone(resultado.dimension)

    def test_rechaza_coeficientes_no_finitos(self):
        with self.assertRaisesRegex(ValueError, "finitos"):
            AnalisadorVectorial.analizar_subespacio_ecuacion(
                float("nan"), 1, 0
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
