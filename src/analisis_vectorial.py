from dataclasses import dataclass

import numpy as np

try:
    from objetos import Objeto2D
except ImportError:
    from .objetos import Objeto2D

EPSILON = 1e-9


@dataclass(frozen=True)
class ResultadoSubespacio:
    """Resultado justificable del análisis del conjunto ax + by = c."""

    ecuacion: str
    es_subespacio: bool
    contiene_cero: bool
    cierre_suma: bool | None
    cierre_escalar: bool | None
    dimension: int | None
    base: np.ndarray
    calculos: tuple[str, ...]
    interpretacion: str


class AnalisadorVectorial:
    def __init__(self, objeto):
        if not isinstance(objeto, Objeto2D):
            raise TypeError("Se requiere un objeto Objeto2D")
        self._objeto = objeto
        self._vectores = objeto.puntos.T

    def _gauss_jordan(self, matriz):
        A = matriz.astype(float).copy()
        m, n = A.shape
        rank = 0
        for col in range(n):
            pivot = -1
            for row in range(rank, m):
                if abs(A[row, col]) > EPSILON:
                    pivot = row
                    break
            if pivot == -1:
                continue
            A[[rank, pivot]] = A[[pivot, rank]]
            A[rank] = A[rank] / A[rank, col]
            for row in range(m):
                if row != rank and abs(A[row, col]) > EPSILON:
                    A[row] -= A[row, col] * A[rank]
            rank += 1
        return A, rank

    def _gaussian_elimination(self, matriz):
        A = matriz.astype(float).copy()
        m, n = A.shape
        rank = 0
        for col in range(n):
            pivot = -1
            for row in range(rank, m):
                if abs(A[row, col]) > EPSILON:
                    pivot = row
                    break
            if pivot == -1:
                continue
            A[[rank, pivot]] = A[[pivot, rank]]
            A[rank] = A[rank] / A[rank, col]
            for row in range(rank + 1, m):
                if abs(A[row, col]) > EPSILON:
                    A[row] -= A[row, col] * A[rank]
            rank += 1
        return A, rank

    def _en_el_span(self, vector, base):
        A = base.astype(float).copy()
        b = np.array(vector, dtype=float)
        m = A.shape[0]
        aug = np.hstack([A, b.reshape(-1, 1)])
        rref, _ = self._gauss_jordan(aug)
        last_col = rref[:, -1]
        for i in range(m):
            if all(abs(rref[i, :-1]) < EPSILON) and abs(last_col[i]) > EPSILON:
                return False
        return True

    def _obtener_matriz(self, vectores):
        if vectores is None:
            return self._vectores.astype(float).copy()
        A = np.array(vectores, dtype=float)
        if A.ndim == 1:
            A = A.reshape(1, -1)
        return A

    def _indices_base(self, matriz):
        """Selecciona una base formada por vectores del conjunto original."""
        indices = []
        rango_actual = 0
        for indice in range(matriz.shape[0]):
            candidatos = matriz[indices + [indice]]
            _, nuevo_rango = self._gaussian_elimination(candidatos)
            if nuevo_rango > rango_actual:
                indices.append(indice)
                rango_actual = nuevo_rango
        return indices

    @staticmethod
    def _contiene_vector(matriz, vector):
        """Comprueba pertenencia al conjunto finito, con tolerancia numérica."""
        return any(np.allclose(fila, vector, atol=EPSILON, rtol=0.0) for fila in matriz)

    def es_linealmente_independiente(self, vectores=None):
        A = self._obtener_matriz(vectores)
        _, rank = self._gauss_jordan(A)
        return rank == A.shape[0]

    def encontrar_base(self, vectores=None):
        A = self._obtener_matriz(vectores)
        return A[self._indices_base(A)].copy()

    def detectar_redundantes(self, vectores=None):
        A = self._obtener_matriz(vectores)
        indices_base = set(self._indices_base(A))
        return [indice for indice in range(A.shape[0]) if indice not in indices_base]

    def verificar_cierre_suma(self, vectores=None):
        """Verifica cierre de la colección finita de vectores bajo suma.

        Esto deliberadamente comprueba pertenencia al conjunto recibido, no a
        su espacio generado: el span siempre sería cerrado y la prueba no
        aportaría información.
        """
        A = self._obtener_matriz(vectores)
        for i in range(A.shape[0]):
            for j in range(i, A.shape[0]):
                suma = A[i] + A[j]
                if not self._contiene_vector(A, suma):
                    return False
        return True

    def verificar_cierre_escalar(self, vectores=None, escalares=None):
        """Evalúa cierre para una muestra explícita de escalares.

        Una colección finita no nula nunca puede ser un subespacio real. La
        muestra permite exhibir contraejemplos concretos sin afirmar que se
        enumeraron todos los escalares de R.
        """
        A = self._obtener_matriz(vectores)
        if escalares is None:
            escalares = [0, 1, -1, 2, -2, 0.5]
        for v in A:
            for c in escalares:
                prod = c * v
                if not self._contiene_vector(A, prod):
                    return False
        return True

    def calcular_dimension(self, vectores=None):
        A = self._obtener_matriz(vectores)
        _, rank = self._gaussian_elimination(A)
        return rank

    @staticmethod
    def analizar_subespacio_ecuacion(a, b, c=0.0):
        """Analiza si ``S={(x,y): ax+by=c}`` es subespacio de R².

        Además del veredicto, devuelve las comprobaciones simbólicas o un
        contraejemplo concreto para el vector cero, la suma y el producto
        escalar. Esto permite justificar casos como ``x + y = 10`` sin
        confundir la ecuación del escenario con su conjunto finito de vértices.
        """
        coeficientes = np.asarray([a, b, c], dtype=float)
        if not np.isfinite(coeficientes).all():
            raise ValueError("Los coeficientes a, b y c deben ser números finitos")
        a, b, c = (float(valor) for valor in coeficientes)
        ecuacion = f"{a:g}x + {b:g}y = {c:g}"

        normal_nulo = abs(a) <= EPSILON and abs(b) <= EPSILON
        termino_independiente_nulo = abs(c) <= EPSILON

        if normal_nulo and termino_independiente_nulo:
            return ResultadoSubespacio(
                ecuacion=ecuacion,
                es_subespacio=True,
                contiene_cero=True,
                cierre_suma=True,
                cierre_escalar=True,
                dimension=2,
                base=np.eye(2, dtype=float),
                calculos=(
                    "La igualdad 0 = 0 se cumple para todo vector (x, y).",
                    "Vector cero: 0 = 0, por lo tanto (0, 0) pertenece al conjunto.",
                    "Suma: la suma de dos vectores de R² sigue perteneciendo a R².",
                    "Producto escalar: λu pertenece a R² para todo λ real.",
                ),
                interpretacion=(
                    "El conjunto solución es todo R²; es un espacio vectorial "
                    "de dimensión 2."
                ),
            )

        if normal_nulo:
            return ResultadoSubespacio(
                ecuacion=ecuacion,
                es_subespacio=False,
                contiene_cero=False,
                cierre_suma=None,
                cierre_escalar=None,
                dimension=None,
                base=np.empty((0, 2), dtype=float),
                calculos=(
                    f"La igualdad 0 = {c:g} es imposible.",
                    "El conjunto solución es vacío y no contiene al vector cero.",
                    "Sin vectores en el conjunto, no corresponde buscar una base o dimensión.",
                ),
                interpretacion=(
                    "El conjunto solución es vacío, por lo que no puede ser "
                    "un subespacio vectorial."
                ),
            )

        if termino_independiente_nulo:
            generador = np.array([[-b, a]], dtype=float)
            return ResultadoSubespacio(
                ecuacion=ecuacion,
                es_subespacio=True,
                contiene_cero=True,
                cierre_suma=True,
                cierre_escalar=True,
                dimension=1,
                base=generador,
                calculos=(
                    "Vector cero: a·0 + b·0 = 0, así que (0, 0) pertenece.",
                    (
                        "Suma: si au₁+bu₂=0 y av₁+bv₂=0, entonces "
                        "a(u₁+v₁)+b(u₂+v₂)=0+0=0."
                    ),
                    (
                        "Producto escalar: si au₁+bu₂=0, entonces "
                        "a(λu₁)+b(λu₂)=λ·0=0."
                    ),
                    (
                        f"El vector ({-b:g}, {a:g}) satisface la ecuación y "
                        "genera toda la recta."
                    ),
                ),
                interpretacion=(
                    "Es una recta que pasa por el origen; por ello es un "
                    "subespacio de R² de dimensión 1."
                ),
            )

        if abs(a) > EPSILON:
            punto = np.array([c / a, 0.0], dtype=float)
        else:
            punto = np.array([0.0, c / b], dtype=float)
        doble = 2.0 * punto
        lhs_punto = a * punto[0] + b * punto[1]
        lhs_doble = a * doble[0] + b * doble[1]
        punto_texto = f"({punto[0]:g}, {punto[1]:g})"
        doble_texto = f"({doble[0]:g}, {doble[1]:g})"

        return ResultadoSubespacio(
            ecuacion=ecuacion,
            es_subespacio=False,
            contiene_cero=False,
            cierre_suma=False,
            cierre_escalar=False,
            dimension=None,
            base=np.empty((0, 2), dtype=float),
            calculos=(
                (
                    f"Vector cero: a·0 + b·0 = 0 ≠ {c:g}; "
                    "(0, 0) no pertenece."
                ),
                (
                    f"Tomamos p={punto_texto}: ap₁+bp₂={lhs_punto:g}, "
                    "por lo tanto p sí pertenece."
                ),
                (
                    f"Suma: p+p={doble_texto} y su lado izquierdo vale "
                    f"{lhs_doble:g} ≠ {c:g}; no hay cierre bajo suma."
                ),
                (
                    f"Producto escalar: 2p={doble_texto} tampoco pertenece; "
                    "no hay cierre bajo multiplicación escalar."
                ),
            ),
            interpretacion=(
                "Es una recta afín que no pasa por el origen. Puede describir "
                "posiciones válidas, pero no es un subespacio vectorial."
            ),
        )
