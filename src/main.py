

import numpy as np

try:
    from analisis_vectorial import AnalisadorVectorial
    from historial import aplicar_transformaciones_consecutivas
    from objetos import crear_cuadrado
except ImportError:
    from .analisis_vectorial import AnalisadorVectorial
    from .historial import aplicar_transformaciones_consecutivas
    from .objetos import crear_cuadrado


def mostrar_historial(historial):
    print("\nHISTORIAL DE TRANSFORMACIONES")
    print("=" * 60)
    for numero, registro in enumerate(historial.registros, start=1):
        print(f"\n{numero}. {registro.nombre}")
        print("Estado anterior (2xN):")
        print(np.round(registro.estado_antes, 6))
        print("Matriz utilizada:")
        print(np.round(registro.matriz, 6))
        print("Estado posterior (2xN):")
        print(np.round(registro.estado_despues, 6))

    print("\nMatriz compuesta homogénea T @ S @ R:")
    print(np.round(historial.matriz_compuesta(), 6))


def ejecutar_flujo_principal():
    objeto = crear_cuadrado(lado=2.0, origen=(0.0, 0.0))
    print("OBJETO CREADO")
    print(objeto)

    objeto_final, historial = aplicar_transformaciones_consecutivas(objeto)
    mostrar_historial(historial)

    analisis = AnalisadorVectorial(objeto_final)
    resultados = {
        "linealmente_independiente": analisis.es_linealmente_independiente(),
        "base": analisis.encontrar_base(),
        "dimension": analisis.calcular_dimension(),
        "redundantes": analisis.detectar_redundantes(),
        "cierre_suma": analisis.verificar_cierre_suma(),
        "cierre_escalar": analisis.verificar_cierre_escalar(),
    }

    print("\nANÁLISIS VECTORIAL DEL OBJETO FINAL")
    print("=" * 60)
    print(objeto_final)
    print(f"Linealmente independiente: {resultados['linealmente_independiente']}")
    print(f"Base:\n{np.round(resultados['base'], 6)}")
    print(f"Dimensión: {resultados['dimension']}")
    print(f"Índices redundantes: {resultados['redundantes']}")
    print(f"Cierre bajo suma: {resultados['cierre_suma']}")
    print(f"Cierre bajo producto escalar: {resultados['cierre_escalar']}")
    return objeto_final, historial, resultados


if __name__ == "__main__":
    ejecutar_flujo_principal()

