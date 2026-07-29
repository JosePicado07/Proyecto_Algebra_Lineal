import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from objetos import (
    Objeto2D,
    crear_cuadrado,
    crear_triangulo,
    crear_rectangulo,
)
from analisis_vectorial import AnalisadorVectorial

print("=" * 60)
print("TEST: Caso 1 - Crear cuadrado y verificar coordenadas")
print("=" * 60)

cuad = crear_cuadrado(lado=2.0, origen=(0.0, 0.0))
print(cuad)

xs, ys = cuad.obtener_xy()
print(f"xs = {xs}")
print(f"ys = {ys}")

assert cuad.n == 4, f"El cuadrado debe tener 4 puntos, tiene {cuad.n}"
assert cuad.nombre == "Cuadrado"
assert xs[0] == 0.0 and ys[0] == 0.0
assert xs[1] == 2.0 and ys[1] == 0.0
assert xs[2] == 2.0 and ys[2] == 2.0
assert xs[3] == 0.0 and ys[3] == 2.0

print("[OK] Caso 1: Cuadrado creado correctamente")

print()
print("=" * 60)
print("TEST: Caso 2 - Clonar triangulo y verificar copia independiente")
print("=" * 60)

tri = crear_triangulo(base=4.0, altura=3.0, origen=(1.0, 1.0))
copia = tri.clonar()

print(f"Original: {tri}")
print(f"Copia:    {copia}")

tri.puntos[0, 0] = 999.0

assert copia.puntos[0, 0] != tri.puntos[0, 0], (
    "La copia no debe modificarse al cambiar el original"
)
assert copia.puntos[0, 0] == 1.0, (
    f"El primer x de la copia debe seguir siendo 1.0, pero es {copia.puntos[0, 0]}"
)
assert tri.nombre == "Triangulo"
assert copia.nombre == "Triangulo_copia"

print("[OK] Caso 2: Clonacion funciona, copia independiente del original")

print()
print("=" * 60)
print("TEST: Caso 3 - Crear objeto desde lista de tuplas")
print("=" * 60)

lista_tuplas = [(10.0, 20.0), (30.0, 40.0), (50.0, 60.0)]
obj = Objeto2D(lista_tuplas, nombre="ListaTest")
print(obj)

assert obj.n == 3
assert obj.puntos.shape == (2, 3)
assert obj.puntos[0, 0] == 10.0
assert obj.puntos[1, 0] == 20.0
assert obj.puntos[0, 1] == 30.0
assert obj.puntos[1, 1] == 40.0
assert obj.puntos[0, 2] == 50.0
assert obj.puntos[1, 2] == 60.0

tuplas_devueltas = obj.to_lista_tuplas()
assert tuplas_devueltas == lista_tuplas, (
    f"to_lista_tuplas() debe devolver {lista_tuplas}, pero devolvio {tuplas_devueltas}"
)

print(f"Matriz interna (2xN):\n{obj.puntos}")
print(f"to_lista_tuplas(): {tuplas_devueltas}")
print("[OK] Caso 3: Lista de tuplas convertida correctamente a matriz 2xN")

print()
print("=" * 60)
print("TEST: Verificaciones adicionales")
print("=" * 60)

rect = crear_rectangulo(ancho=5.0, alto=3.0, origen=(-1.0, -1.0))
print(rect)
assert rect.n == 4
assert rect.nombre == "Rectangulo"
xs, ys = rect.obtener_xy()
assert xs[2] - xs[1] == 0.0

print(f"__len__: {len(rect)}")

print("[OK] Todas las verificaciones adicionales pasaron")

print()
print("=" * 60)
print("TEST: es_linealmente_independiente")
print("=" * 60)

v_ld = Objeto2D([(0,0), (1,0), (0,1)], nombre="LD_test")
av = AnalisadorVectorial(v_ld)
assert av.es_linealmente_independiente() == False
print(f"[(0,0),(1,0),(0,1)] LI? {av.es_linealmente_independiente()}")

v_li = Objeto2D([(1,0), (0,1)], nombre="LI_test")
av2 = AnalisadorVectorial(v_li)
assert av2.es_linealmente_independiente() == True
print(f"[(1,0),(0,1)] LI? {av2.es_linealmente_independiente()}")

v_ld2 = Objeto2D([(1,0), (2,0)], nombre="LD2_test")
av3 = AnalisadorVectorial(v_ld2)
assert av3.es_linealmente_independiente() == False
print(f"[(1,0),(2,0)] LI? {av3.es_linealmente_independiente()}")

print("[OK] es_linealmente_independiente funciona")

print()
print("=" * 60)
print("TEST: encontrar_base + calcular_dimension (6 puntos en R2)")
print("=" * 60)

seis_puntos = Objeto2D([
    (1, 0), (0, 1), (2, 0), (0, 2), (1, 1), (3, 0)
], nombre="6puntos")
av4 = AnalisadorVectorial(seis_puntos)
base = av4.encontrar_base()
dim = av4.calcular_dimension()
print(f"Base ({base.shape[0]} vectores):\n{base}")
print(f"Dimension: {dim}")
assert base.shape[0] == 2
assert dim == 2
print("[OK] Base y dimension correctas (dim=2 en R2)")

print()
print("=" * 60)
print("TEST: detectar_redundantes")
print("=" * 60)

redundantes = av4.detectar_redundantes()
print(f"Indices redundantes: {redundantes}")
assert redundantes == [2, 3, 4, 5]
assert np.array_equal(base, np.array([[1.0, 0.0], [0.0, 1.0]]))
print("[OK] Redundancia detectada")

print()
print("=" * 60)
print("TEST: verificar_cierre_suma y verificar_cierre_escalar")
print("=" * 60)

base_ej = Objeto2D([(1,0), (0,1), (2,2)], nombre="base_ej")
av5 = AnalisadorVectorial(base_ej)
cs = av5.verificar_cierre_suma()
ce = av5.verificar_cierre_escalar()
print(f"Cierre suma: {cs}, Cierre escalar: {ce}")
assert cs == False
assert ce == False

solo_cero = AnalisadorVectorial(Objeto2D([(0, 0)], nombre="Subespacio cero"))
assert solo_cero.verificar_cierre_suma() == True
assert solo_cero.verificar_cierre_escalar() == True
print("[OK] El conjunto finito se distingue de su espacio generado")

print()
print("=" * 60)
print("TEST: Triangulo con punto interior (redundante)")
print("=" * 60)

tri_centro = Objeto2D([
    (0, 0), (2, 0), (1, 1.732), (1, 0.577)
], nombre="Triangulo+centro")
av6 = AnalisadorVectorial(tri_centro)
dim6 = av6.calcular_dimension()
base6 = av6.encontrar_base()
red6 = av6.detectar_redundantes()
print(f"Dimension: {dim6}")
print(f"Base:\n{base6}")
print(f"Redundantes (indices): {red6}")
assert dim6 == 2
assert red6 == [0, 3]
assert 3 in red6
print("[OK] Punto interior detectado como redundante")

print()
print("=" * 60)
print("TODOS LOS TESTS PASARON")
print("=" * 60)
