"""Pruebas de la lógica que alimenta la interfaz de Antonio."""

import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from interfaz import Motor2DController, guardar_comparacion


class TestMotor2DController(unittest.TestCase):
    def test_aplica_transformaciones_consecutivas_y_conserva_original(self):
        controlador = Motor2DController()
        original = controlador.objeto_original.puntos.copy()

        controlador.aplicar_transformacion("Rotar", angulo=30)
        controlador.aplicar_transformacion("Escalar", sx=1.5, sy=1.5)
        controlador.aplicar_transformacion("Trasladar", dx=2, dy=1)

        self.assertEqual(len(controlador.historial), 3)
        np.testing.assert_array_equal(controlador.objeto_original.puntos, original)
        reconstruido = controlador.historial.reconstruir_estado_final(
            controlador.objeto_original
        )
        np.testing.assert_allclose(
            reconstruido.puntos, controlador.objeto_actual.puntos, atol=1e-9
        )

    def test_figura_personalizada_y_analisis(self):
        controlador = Motor2DController()
        controlador.crear_figura(
            "Personalizada", puntos="1,0; 0,1; 2,0; 0,2"
        )
        resultado = controlador.analizar()

        self.assertEqual(controlador.objeto_actual.n, 4)
        self.assertEqual(resultado.dimension, 2)
        self.assertFalse(resultado.linealmente_independiente)
        self.assertGreaterEqual(len(resultado.redundantes), 2)

    def test_reiniciar_restaura_figura_y_limpia_historial(self):
        controlador = Motor2DController()
        controlador.aplicar_transformacion("Reflejar", eje="y")
        controlador.reiniciar_transformaciones()

        self.assertEqual(len(controlador.historial), 0)
        np.testing.assert_array_equal(
            controlador.objeto_actual.puntos,
            controlador.objeto_original.puntos,
        )

    def test_validacion_de_puntos_personalizados(self):
        self.assertEqual(
            Motor2DController.parsear_puntos("0,0; 2,0; 1,1"),
            [(0.0, 0.0), (2.0, 0.0), (1.0, 1.0)],
        )
        with self.assertRaisesRegex(ValueError, "al menos 3"):
            Motor2DController.parsear_puntos("0,0; 1,1")
        with self.assertRaisesRegex(ValueError, "formato"):
            Motor2DController.parsear_puntos("0,0; 1; 2,2")

    def test_exporta_grafico(self):
        controlador = Motor2DController()
        controlador.aplicar_transformacion("Rotar", angulo=45)
        destino = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "_comparacion_temporal.png",
        )
        try:
            guardar_comparacion(
                destino,
                controlador.objeto_original,
                controlador.objeto_actual,
            )
            self.assertTrue(os.path.exists(destino))
            self.assertGreater(os.path.getsize(destino), 0)
        finally:
            if os.path.exists(destino):
                os.remove(destino)


if __name__ == "__main__":
    unittest.main(verbosity=2)
