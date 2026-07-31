# PixelForge MathEngine 2D v1.0

Prototipo académico de un motor matemático para representar figuras 2D,
aplicar transformaciones geométricas, conservar su historial y analizar los
vectores resultantes. El proyecto fue desarrollado para el curso FUN-06
Álgebra Lineal de la Universidad CENFOTEC.

## Funcionalidades

- Figuras predefinidas: cuadrado, triángulo y rectángulo.
- Figuras personalizadas mediante coordenadas `x,y; x,y; ...`.
- Traslación, rotación, escalamiento y reflexión.
- Transformaciones consecutivas con historial de matrices y estados.
- Matriz homogénea compuesta para reconstruir el resultado final.
- Análisis de independencia lineal, base, dimensión y redundancia.
- Verificación de cierre del conjunto finito de vértices bajo suma y una
  muestra explícita de multiplicaciones escalares.
- Análisis de conjuntos definidos por `ax + by = c`, con verificación de
  subespacio, base, dimensión, cálculos y contraejemplos.
- Interfaz Tkinter con gráficos Matplotlib del estado original y transformado.
- Modo de demostración por consola para entornos sin interfaz gráfica.

## Requisitos

- Python 3.10 o superior.
- Tkinter, incluido normalmente con Python en Windows y macOS.
- Dependencias indicadas en `requirements.txt`.

En Linux, Tkinter puede requerir un paquete del sistema, por ejemplo
`python3-tk`.

## Instalación

Desde la carpeta raíz del proyecto, en Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Ejecutar la interfaz

```bash
python3 src/interfaz.py
```

En Windows puede sustituir `python3` por `python`.

La ventana permite:

1. Escoger o crear la figura.
2. Indicar los parámetros de una transformación.
3. Aplicar varias operaciones seguidas.
4. Comparar los gráficos original y transformado.
5. Consultar coordenadas, última matriz, análisis e historial.
6. Consultar el desarrollo matricial de la última operación.
7. Analizar en la pestaña `Subespacio` una restricción como `x + y = 10`,
   ingresando `a=1`, `b=1` y `c=10`.
8. Exportar la comparación como imagen PNG.

Para una figura personalizada, ingrese al menos tres puntos separados por
punto y coma:

```text
0,0; 3,0; 2,2; 0,2
```

## Demostración sin GUI

El caso solicitado en la consigna rota 30 grados, escala por 1.5 y traslada
por `(2, 1)`:

```bash
python3 src/interfaz.py --demo
```

También puede guardar el gráfico:

```bash
python3 src/interfaz.py --demo --grafico comparacion.png
```

El flujo integrado original continúa disponible:

```bash
python3 src/main.py
```

## Pruebas

Ejecute todas las pruebas con:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

La verificación cubre creación y clonación de objetos, algoritmos de análisis,
las cuatro transformaciones, composición e historial, integración completa y
la lógica independiente de la interfaz. También valida rectas homogéneas,
rectas afines, todo `R²` y el conjunto vacío en el análisis de subespacios.

## Documentación final

Las fuentes editables están en `docs/informe_tecnico.md` y
`docs/bitacora_ia_grupal.md`. Para volver a generar los PDF y sus figuras:

```bash
python3 docs/generar_documentacion.py
```

El comando produce `Informe_Tecnico.pdf`, `Bitacora_IA_Grupal.pdf` y los
recursos gráficos de `docs/assets/`.

## Estructura

```text
Proyecto_Algebra_Lineal/
├── src/
│   ├── objetos.py
│   ├── transformaciones.py
│   ├── analisis_vectorial.py
│   ├── historial.py
│   ├── interfaz.py
│   └── main.py
├── tests/
│   ├── test_analisis.py
│   ├── test_transformaciones.py
│   ├── test_integracion.py
│   ├── test_subespacios.py
│   └── test_interfaz.py
├── docs/
│   ├── bitacoras/
│   ├── explicaciones/
│   ├── pseudocodigos/
│   ├── assets/
│   ├── informe_tecnico.md
│   ├── bitacora_ia_grupal.md
│   └── MATRIZ_CUMPLIMIENTO.md
├── Informe_Tecnico.pdf
├── Bitacora_IA_Grupal.pdf
├── requirements.txt
└── README.md
```

## Decisiones matemáticas

Los puntos se almacenan como una matriz `2×N`, con un vértice por columna. Las
transformaciones lineales se aplican con el operador matricial `@`. La
traslación usa coordenadas homogéneas `3×3`. El análisis de rango, base e
independencia utiliza eliminaciones propias; no emplea
`numpy.linalg.matrix_rank`, `numpy.linalg.inv` ni `numpy.linalg.eig`.

El programa distingue entre el conjunto finito de vértices y el espacio
vectorial que esos vértices generan. La base y la dimensión corresponden al
espacio generado. El cierre bajo suma se comprueba contra el conjunto finito;
el cierre escalar se evalúa con los escalares `0`, `±1`, `±2` y `0.5`. Esta
última comprobación encuentra contraejemplos útiles, pero no pretende enumerar
todos los escalares reales.

Las restricciones de posiciones se analizan por separado como conjuntos
solución de `ax + by = c`. Si `c=0`, una ecuación no trivial describe una recta
por el origen y sí es un subespacio de dimensión 1. Si `c≠0`, describe una
recta afín que no contiene al vector cero; el programa muestra un punto del
conjunto y comprueba que su suma consigo mismo y su múltiplo por 2 no
pertenecen.

## Solución de problemas

- Si aparece `ModuleNotFoundError`, active el entorno virtual y repita
  `python -m pip install -r requirements.txt`.
- Si Tkinter no abre en Linux, instale el paquete `python3-tk` correspondiente
  a su distribución.
- Si trabaja en un servidor sin pantalla, use el modo `--demo`.
- Los ángulos se ingresan en grados y los ejes de reflexión válidos son `x`,
  `y` y `y=x`.
