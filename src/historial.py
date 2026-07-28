"""Registro y composición de las transformaciones aplicadas a un Objeto2D."""

from dataclasses import dataclass

import numpy as np

try:
    from objetos import Objeto2D
    from transformaciones import Transformador
except ImportError:
    from .objetos import Objeto2D
    from .transformaciones import Transformador


@dataclass(frozen=True)
class RegistroTransformacion:
    """Copia independiente de una modificación realizada sobre el objeto."""

    nombre: str
    matriz: np.ndarray
    estado_antes: np.ndarray
    estado_despues: np.ndarray


class HistorialTransformaciones:
    """Guarda la matriz y el estado anterior/posterior de cada transformación."""

    def __init__(self):
        self._registros = []

    @staticmethod
    def _validar_objeto(objeto):
        if not isinstance(objeto, Objeto2D):
            raise TypeError("El estado debe pertenecer a un Objeto2D")

    @staticmethod
    def _matriz_homogenea(matriz):
        """Convierte una matriz lineal 2x2 en homogénea 3x3."""
        matriz = np.asarray(matriz, dtype=np.float64)
        if matriz.shape == (3, 3):
            return matriz.copy()
        if matriz.shape == (2, 2):
            resultado = np.eye(3, dtype=np.float64)
            resultado[:2, :2] = matriz
            return resultado
        raise ValueError("La matriz debe tener dimensiones 2x2 o 3x3")

    def registrar(self, nombre, matriz, objeto_antes, objeto_despues):
        self._validar_objeto(objeto_antes)
        self._validar_objeto(objeto_despues)
        registro = RegistroTransformacion(
            nombre=str(nombre),
            matriz=np.asarray(matriz, dtype=np.float64).copy(),
            estado_antes=objeto_antes.puntos.copy(),
            estado_despues=objeto_despues.puntos.copy(),
        )
        self._registros.append(registro)
        return registro

    @property
    def registros(self):
        return tuple(self._registros)

    def __len__(self):
        return len(self._registros)

    def limpiar(self):
        self._registros.clear()

    def matriz_compuesta(self):
        """Devuelve una matriz 3x3 equivalente a todo el historial."""
        compuesta = np.eye(3, dtype=np.float64)
        for registro in self._registros:
            compuesta = self._matriz_homogenea(registro.matriz) @ compuesta
        return compuesta

    def reconstruir_estado_final(self, objeto_inicial):
        """Aplica la composición al objeto inicial para reconstruir el resultado."""
        self._validar_objeto(objeto_inicial)
        puntos_h = np.vstack(
            [objeto_inicial.puntos, np.ones((1, objeto_inicial.n), dtype=np.float64)]
        )
        puntos_finales = (self.matriz_compuesta() @ puntos_h)[:2, :]
        return Objeto2D(puntos_finales, nombre=f"{objeto_inicial.nombre}_reconstruido")


def aplicar_y_registrar(historial, nombre, objeto_antes, resultado_transformacion):
    """Registra el resultado `(Objeto2D, matriz)` devuelto por Transformador."""
    objeto_despues, matriz = resultado_transformacion
    historial.registrar(nombre, matriz, objeto_antes, objeto_despues)
    return objeto_despues


def aplicar_transformaciones_consecutivas(
    objeto, transformador=None, historial=None, traslacion=(2.0, 1.0)
):
    """Rota 30°, escala 1.5 y traslada, registrando cada paso."""
    if not isinstance(objeto, Objeto2D):
        raise TypeError("Se requiere un objeto de tipo Objeto2D")
    transformador = transformador or Transformador()
    historial = historial or HistorialTransformaciones()

    rotado = aplicar_y_registrar(
        historial,
        "Rotación 30°",
        objeto,
        transformador.rotar(objeto, 30.0),
    )
    escalado = aplicar_y_registrar(
        historial,
        "Escalamiento uniforme 1.5",
        rotado,
        transformador.escalar(rotado, 1.5),
    )
    final = aplicar_y_registrar(
        historial,
        f"Traslación dx={traslacion[0]}, dy={traslacion[1]}",
        escalado,
        transformador.trasladar(escalado, *traslacion),
    )
    return final, historial

