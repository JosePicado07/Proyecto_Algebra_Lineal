import numpy as np

class Objeto2D:
    def __init__(self, puntos, nombre="Figura"):
        self.nombre = nombre
        arr = self._convertir_a_matriz(puntos)
        if arr.shape[1] == 0:
            raise ValueError("El objeto debe contener al menos un punto")
        if not np.isfinite(arr).all():
            raise ValueError("Las coordenadas deben ser números finitos")
        self.puntos = arr
        self.n = arr.shape[1]

    def _convertir_a_matriz(self, puntos):
        if isinstance(puntos, np.ndarray):
            if puntos.ndim != 2:
                raise ValueError("El array debe ser 2-dimensional")
            if puntos.shape[0] == 2:
                return puntos.astype(np.float64)
            elif puntos.shape[1] == 2:
                return puntos.T.astype(np.float64)
            else:
                raise ValueError(
                    f"Formato de array no reconocido: {puntos.shape}. "
                    "Se espera (2, N) o (N, 2)"
                )
        if isinstance(puntos, (list, tuple)):
            arr = np.array(puntos, dtype=np.float64)
            if arr.ndim != 2 or arr.shape[1] != 2:
                raise ValueError(
                    "La lista debe contener pares (x, y), ej: [(x1,y1), (x2,y2), ...]"
                )
            return arr.T
        raise TypeError("puntos debe ser ndarray, list o tuple")

    def clonar(self):
        return Objeto2D(np.copy(self.puntos), nombre=self.nombre + "_copia")

    def obtener_xy(self):
        return self.puntos[0], self.puntos[1]

    def __str__(self):
        tuplas = self.to_lista_tuplas()
        pts_str = " ".join(f"({x:.2f},{y:.2f})" for x, y in tuplas)
        return f"{self.nombre}: {pts_str}"

    def to_lista_tuplas(self):
        return [(float(self.puntos[0, i]), float(self.puntos[1, i]))
                for i in range(self.n)]

    def __len__(self):
        return self.n

    def __repr__(self):
        return (f"Objeto2D(nombre='{self.nombre}', n={self.n}, "
                f"shape={self.puntos.shape})\n{self.puntos}")


def crear_cuadrado(lado=2.0, origen=(0.0, 0.0)):
    lado = float(lado)
    if not np.isfinite(lado) or lado <= 0:
        raise ValueError("El lado debe ser un número finito mayor que cero")
    x0, y0 = origen
    pts = [
        [x0,       y0],
        [x0 + lado, y0],
        [x0 + lado, y0 + lado],
        [x0,       y0 + lado],
    ]
    return Objeto2D(pts, nombre="Cuadrado")


def crear_triangulo(base=2.0, altura=2.0, origen=(0.0, 0.0)):
    base, altura = float(base), float(altura)
    if not np.isfinite([base, altura]).all() or base <= 0 or altura <= 0:
        raise ValueError("La base y la altura deben ser números finitos mayores que cero")
    x0, y0 = origen
    pts = [
        [x0,          y0],
        [x0 + base,   y0],
        [x0 + base/2, y0 + altura],
    ]
    return Objeto2D(pts, nombre="Triangulo")


def crear_rectangulo(ancho=3.0, alto=2.0, origen=(0.0, 0.0)):
    ancho, alto = float(ancho), float(alto)
    if not np.isfinite([ancho, alto]).all() or ancho <= 0 or alto <= 0:
        raise ValueError("El ancho y el alto deben ser números finitos mayores que cero")
    x0, y0 = origen
    pts = [
        [x0,        y0],
        [x0 + ancho, y0],
        [x0 + ancho, y0 + alto],
        [x0,        y0 + alto],
    ]
    return Objeto2D(pts, nombre="Rectangulo")
