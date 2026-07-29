import math
import numpy as np

try:
    from objetos import Objeto2D
except ImportError:
    from .objetos import Objeto2D


class Transformador:
    """
    Aplica transformaciones geométricas 2D a objetos representados como
    matrices 2xN.

    Cada columna de objeto.puntos representa un vértice:
        p_i = (x_i, y_i)^T

    Restricción del proyecto:
    - Se usan operaciones matriciales básicas de NumPy.
    - No se usan funciones directas prohibidas como numpy.linalg.inv,
      numpy.linalg.eig o numpy.linalg.matrix_rank.
    """

    def __init__(self):
        self.ultima_matriz = None
        self.ultima_operacion = None

    def _validar_objeto(self, objeto):
        if not isinstance(objeto, Objeto2D):
            raise TypeError("Se requiere un objeto de tipo Objeto2D")
        if objeto.puntos.shape[0] != 2:
            raise ValueError("El objeto debe almacenar sus puntos en formato 2xN")

    def _crear_objeto_transformado(self, objeto, puntos_transformados, sufijo):
        return Objeto2D(
            np.array(puntos_transformados, dtype=np.float64),
            nombre=f"{objeto.nombre}_{sufijo}",
        )

    @staticmethod
    def _numero_finito(valor, nombre):
        numero = float(valor)
        if not math.isfinite(numero):
            raise ValueError(f"{nombre} debe ser un número finito")
        return numero

    def trasladar(self, objeto, dx, dy):
        """
        Aplica una traslación usando coordenadas homogéneas.

        Matriz:
            [1  0  dx]
        T = [0  1  dy]
            [0  0   1]

        Como la traslación no es una transformación lineal pura en R²,
        se utiliza una matriz homogénea 3x3.
        """
        self._validar_objeto(objeto)
        dx = self._numero_finito(dx, "dx")
        dy = self._numero_finito(dy, "dy")

        matriz = np.array(
            [
                [1.0, 0.0, dx],
                [0.0, 1.0, dy],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float64,
        )

        unos = np.ones((1, objeto.n), dtype=np.float64)
        puntos_homogeneos = np.vstack([objeto.puntos, unos])
        puntos_transformados_h = matriz @ puntos_homogeneos
        puntos_transformados = puntos_transformados_h[:2, :]

        self.ultima_matriz = matriz
        self.ultima_operacion = f"Traslación dx={dx}, dy={dy}"

        return (
            self._crear_objeto_transformado(objeto, puntos_transformados, "trasladado"),
            matriz,
        )

    def rotar(self, objeto, angulo):
        """
        Aplica una rotación alrededor del origen.

        El ángulo se recibe en grados.

        Matriz:
            [cos(theta)  -sen(theta)]
        R = [sen(theta)   cos(theta)]
        """
        self._validar_objeto(objeto)

        angulo = self._numero_finito(angulo, "El ángulo")
        theta = math.radians(angulo)
        c = math.cos(theta)
        s = math.sin(theta)

        matriz = np.array(
            [
                [c, -s],
                [s,  c],
            ],
            dtype=np.float64,
        )

        puntos_transformados = matriz @ objeto.puntos

        self.ultima_matriz = matriz
        self.ultima_operacion = f"Rotación {angulo} grados"

        return (
            self._crear_objeto_transformado(objeto, puntos_transformados, "rotado"),
            matriz,
        )

    def escalar(self, objeto, sx, sy=None):
        """
        Aplica escalamiento respecto al origen.

        Si sy no se indica, se usa el mismo factor que sx
        para realizar escalamiento uniforme.

        Matriz:
            [sx  0 ]
        S = [0   sy]
        """
        self._validar_objeto(objeto)

        if sy is None:
            sy = sx
        sx = self._numero_finito(sx, "sx")
        sy = self._numero_finito(sy, "sy")

        matriz = np.array(
            [
                [sx, 0.0],
                [0.0, sy],
            ],
            dtype=np.float64,
        )

        puntos_transformados = matriz @ objeto.puntos

        self.ultima_matriz = matriz
        self.ultima_operacion = f"Escalamiento sx={sx}, sy={sy}"

        return (
            self._crear_objeto_transformado(objeto, puntos_transformados, "escalado"),
            matriz,
        )

    def reflejar(self, objeto, eje):
        """
        Aplica reflexión respecto al eje indicado.

        Ejes soportados:
        - "x"   o "eje x"
        - "y"   o "eje y"
        - "y=x" o "diagonal"
        """
        self._validar_objeto(objeto)

        eje_normalizado = str(eje).lower().replace(" ", "")

        if eje_normalizado in ("x", "ejex"):
            matriz = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.float64)
            nombre_eje = "eje_x"
        elif eje_normalizado in ("y", "ejey"):
            matriz = np.array([[-1.0, 0.0], [0.0, 1.0]], dtype=np.float64)
            nombre_eje = "eje_y"
        elif eje_normalizado in ("y=x", "x=y", "diagonal"):
            matriz = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.float64)
            nombre_eje = "y_igual_x"
        else:
            raise ValueError("Eje no soportado. Use 'x', 'y' o 'y=x'.")

        puntos_transformados = matriz @ objeto.puntos

        self.ultima_matriz = matriz
        self.ultima_operacion = f"Reflexión respecto a {eje}"

        return (
            self._crear_objeto_transformado(objeto, puntos_transformados, f"reflejado_{nombre_eje}"),
            matriz,
        )
