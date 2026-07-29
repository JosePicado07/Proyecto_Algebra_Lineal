import numpy as np

try:
    from objetos import Objeto2D
except ImportError:
    from .objetos import Objeto2D

EPSILON = 1e-9

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

    def es_linealmente_independiente(self, vectores=None):
        A = self._obtener_matriz(vectores)
        _, rank = self._gauss_jordan(A)
        return rank == A.shape[0]

    def encontrar_base(self, vectores=None):
        A = self._obtener_matriz(vectores)
        ref, rank = self._gaussian_elimination(A)
        return ref[:rank]

    def detectar_redundantes(self, vectores=None):
        A = self._obtener_matriz(vectores)
        redundantes = []
        for i in range(A.shape[0]):
            resto = np.delete(A, i, axis=0)
            if resto.shape[0] == 0:
                continue
            ref, r = self._gaussian_elimination(resto)
            base_resto = ref[:r]
            if base_resto.shape[0] == 0:
                continue
            if self._en_el_span(A[i], base_resto):
                redundantes.append(i)
        return redundantes

    def verificar_cierre_suma(self, vectores=None):
        A = self._obtener_matriz(vectores)
        ref, r = self._gaussian_elimination(A)
        base = ref[:r]
        if base.shape[0] == 0:
            return True
        for i in range(A.shape[0]):
            for j in range(i, A.shape[0]):
                suma = A[i] + A[j]
                if not self._en_el_span(suma, base):
                    return False
        return True

    def verificar_cierre_escalar(self, vectores=None, escalares=None):
        A = self._obtener_matriz(vectores)
        if escalares is None:
            escalares = [0, 1, -1, 2, -2, 0.5]
        ref, r = self._gaussian_elimination(A)
        base = ref[:r]
        if base.shape[0] == 0:
            return True
        for v in A:
            for c in escalares:
                prod = c * v
                if not self._en_el_span(prod, base):
                    return False
        return True

    def calcular_dimension(self, vectores=None):
        A = self._obtener_matriz(vectores)
        _, rank = self._gaussian_elimination(A)
        return rank
