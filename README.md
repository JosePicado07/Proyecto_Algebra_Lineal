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
- Verificación de cierre bajo suma y multiplicación escalar.
- Interfaz Tkinter con gráficos Matplotlib del estado original y transformado.
- Modo de demostración por consola para entornos sin interfaz gráfica.

## Requisitos

- Python 3.10 o superior.
- Tkinter, incluido normalmente con Python en Windows y macOS.
- Dependencias indicadas en `requirements.txt`.

En Linux, Tkinter puede requerir un paquete del sistema, por ejemplo
`python3-tk`.

## Instalación

Desde la carpeta raíz del proyecto:

```bash
python -m venv .venv
```

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

En macOS o Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Ejecutar la interfaz

```bash
python src/interfaz.py
```

La ventana permite:

1. Escoger o crear la figura.
2. Indicar los parámetros de una transformación.
3. Aplicar varias operaciones seguidas.
4. Comparar los gráficos original y transformado.
5. Consultar coordenadas, última matriz, análisis e historial.
6. Exportar la comparación como imagen PNG.

Para una figura personalizada, ingrese al menos tres puntos separados por
punto y coma:

```text
0,0; 3,0; 2,2; 0,2
```

## Demostración sin GUI

El caso solicitado en la consigna rota 30 grados, escala por 1.5 y traslada
por `(2, 1)`:

```bash
python src/interfaz.py --demo
```

También puede guardar el gráfico:

```bash
python src/interfaz.py --demo --grafico comparacion.png
```

El flujo integrado original continúa disponible:

```bash
python src/main.py
```

## Pruebas

Ejecute todas las pruebas con:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

La verificación cubre creación y clonación de objetos, algoritmos de análisis,
las cuatro transformaciones, composición e historial, integración completa y
la lógica independiente de la interfaz.

## Estructura

```text
PixelForge_v1.0/
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
│   └── test_interfaz.py
├── docs/
│   ├── Informe_Tecnico.pdf
│   ├── Bitacora_IA_Grupal.pdf
│   ├── bitacoras/
│   ├── explicaciones/
│   ├── imagenes/
│   └── pseudocodigos/
├── requirements.txt
└── README.md
```

## Decisiones matemáticas

Los puntos se almacenan como una matriz `2×N`, con un vértice por columna. Las
transformaciones lineales se aplican con el operador matricial `@`. La
traslación usa coordenadas homogéneas `3×3`. El análisis de rango, base e
independencia utiliza eliminaciones propias; no emplea
`numpy.linalg.matrix_rank`, `numpy.linalg.inv` ni `numpy.linalg.eig`.

En el análisis de una colección finita de vértices, las verificaciones de
cierre determinan si las combinaciones evaluadas pertenecen al subespacio
generado por esos vectores. No enumeran todos los elementos de un subespacio
infinito.

## Solución de problemas

- Si aparece `ModuleNotFoundError`, active el entorno virtual y repita
  `python -m pip install -r requirements.txt`.
- Si Tkinter no abre en Linux, instale el paquete `python3-tk` correspondiente
  a su distribución.
- Si trabaja en un servidor sin pantalla, use el modo `--demo`.
- Los ángulos se ingresan en grados y los ejes de reflexión válidos son `x`,
  `y` y `y=x`.

