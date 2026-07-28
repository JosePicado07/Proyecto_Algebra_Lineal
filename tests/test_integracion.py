"""Prueba completa: crear cuadrado, rotar, escalar, registrar y analizar."""

import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from analisis_vectorial import AnalisadorVectorial
from historial import HistorialTransformaciones, aplicar_y_registrar
from objetos import crear_cuadrado
from transformaciones import Transformador


class TestIntegracion(unittest.TestCase):
    def test_crear_rotar_escalar_analizar(self):
        original = crear_cuadrado(lado=2.0)
        transformador = Transformador()
        historial = HistorialTransformaciones()

        rotado = aplicar_y_registrar(
            historial,
            "Rotación 30°",
            original,
            transformador.rotar(original, 30.0),
        )
        escalado = aplicar_y_registrar(
            historial,
            "Escalamiento uniforme 1.5",
            rotado,
            transformador.escalar(rotado, 1.5),
        )
        analisis = AnalisadorVectorial(escalado)

        self.assertEqual(len(historial), 2)
        np.testing.assert_allclose(historial.registros[0].estado_antes, original.puntos)
        np.testing.assert_allclose(historial.registros[1].estado_antes, rotado.puntos)
        self.assertEqual(analisis.calcular_dimension(), 2)

        reconstruido = historial.reconstruir_estado_final(original)
        np.testing.assert_allclose(reconstruido.puntos, escalado.puntos, atol=1e-9)

        estado_guardado = historial.registros[0].estado_antes.copy()
        original.puntos[0, 0] = 999.0
        np.testing.assert_array_equal(
            historial.registros[0].estado_antes, estado_guardado
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

