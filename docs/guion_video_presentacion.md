# Guion — Video de presentación
## PixelForge MathEngine 2D v1.0 · Álgebra Lineal (FUN-06) · Universidad CENFOTEC

**Equipo (orden de presentación):** Jose (1.º), Alejandro, Antonio, Marcos.

**Duración objetivo:** 15–18 minutos. Este guion suma ~17 min con margen.

**Materiales:** PowerPoint **`PixelForge-MathEngine-2D-v10.pptx`** (6
diapositivas) + el programa corriendo en la GUI (`python src/interfaz.py`) y
en consola (`python src/interfaz.py --demo`).

**Regla general:** pasar la diapositiva de cada uno en corto, pero **hablar
con el programa en ejecución**, señalar código y resultados reales, evitar
leer las diapositivas y que **todos participen**.

---

## Mapa del video ↔ PowerPoint

| Integrante | Diapositivas PPT | Contenido en el video | Inicio | Minutos |
|---|---|---|---|---|
| **Jose** | 1 y 2 | Presentación · Arquitectura · Representación y Análisis vectorial | 0:00 | ~8.5 |
| **Alejandro** | 3 | Transformaciones geométricas + Matriz compuesta | 8:30 | ~3.5 |
| **Antonio** | 5 | Interfaz, visualización y documentación (demo GUI) | 12:00 | ~2.5 |
| **Marcos** | 4 y 6 | Historial + Matriz compuesta + IA + Conclusiones | 14:30 | ~2.5 |

Total ≈ **17 min** (deja margen para el cierre y las preguntas).

> Nota: la diapositiva **5** (interfaz) se usa en el bloque de Antonio y la
> **4** (historial) en el de Marcos, porque así está la autoría del PPT
> (Antonio hace interfaz/doc; Marcos hace historial/integración).

---

## BLOQUE 1 — Jose (0:00 – 8:30) · Diapositivas PPT 1 y 2

### 1.1 Presentación del proyecto · **PPT diapositiva 1**
- ▶ Pantalla: «PixelForge MathEngine 2D v1.0 — Proyecto académico FUN-06 Álgebra
  Lineal — Universidad CENFOTEC». Miembros: JOSÉ, ALEJANDRO, MARCOS, ANTONIO.
- Di: nombre; que es un **prototipo de motor matemático** (no un juego); el
  objetivo general: representar, transformar y visualizar objetos 2D como
  matrices y vectores aplicando Álgebra Lineal.
- ▶ Pasar a **PPT diapositiva 3 (no): continuar en 2**.

### 1.2 Arquitectura general del programa
- ▶CLIC: código abierto en el árbol `src/` + diagrama de flujo `Objeto2D →
  Transformador → HistorialTransformaciones → AnalizadorVectorial`.
- ▶CLIC: señalar en `src/` cada archivo y su autor:
  - `objetos.py` (Jose), `transformaciones.py` (Alejandro),
    `analisis_vectorial.py`, `historial.py` (Marcos), `interfaz.py` (Antonio),
    `main.py`.
- Di: `Motor2DController` coordina y Tkinter es solo capa de presentación; el
  flujo del programa es Figura → Transformación → Historial → Análisis.

### 1.3 Representación y Análisis vectorial · **PPT diapositiva 2**
- ▶CLIC: PPT **diapositiva 2** «José · Representación y ANÁLISIS VECTORIAL».
  Mostrar ambos bloques: *Representación matricial* y *Análisis vectorial*.
- Di:
  - Cada vértice es una columna `(x,y)` en una matriz **2×N** (N vértices).
  - Facilita aplicar operaciones lineales a toda la figura de una vez.
  - La independencia lineal y la base dicen cuántos vértices son necesarios;
    la dimensión y la redundancia identifican vértices dependientes/colineales.

### 1.4 Demo en la GUI (a partir de aquí el programa)
- ▶CLIC: `python src/interfaz.py` → se abre la ventana con el cuadrado azul
  «Figura original» y el segundo igual (sin transformar).
- ▶CLIC: panel izquierdo Tipo=**Cuadrado**, Lado=**2**, Origen=0/0 →
  ▶CLIC **«Crear / reiniciar figura»**.
- ▶CLIC: pestaña **Coordenadas** → mostrar «COORDENADAS ORIGINALES (2×N)» =
  `[[0,2,2,0],[0,0,2,2]]`.
- ▶CLIC: abrir `objetos.py` (señalar `_convertir_a_matriz` y `clonar()` con
  `np.copy()`) y `analisis_vectorial.py` (señalar `_gauss_jordan`,
  `_indices_base`, `es_linealmente_independiente`, `detectar_redundantes`).
- ▶CLIC: pestaña **Vectores** → mostrar Independencia / Dimensión / Base /
  Vértices redundantes / Cierre.
- ▶CLIC: pestaña **Subespacio** → `a=1, b=1, c=10` → botón **«Analizar ax + by = c»**
  → recta afín que NO pasa por el origen → **no es subespacio**. Luego `c=0`
  → ▶ **«Analizar…»** → recta por el origen → **subespacio de dimensión 1**.

> Entrega a Alejandro en el minuto 8:30.

---

## BLOQUE 2 — Alejandro Medrano (8:30 – 12:00) · PPT diapositiva 3

### 2.1 Diapositiva 3 · Transformaciones con matrices
- ▶CLIC: PPT **diapositiva 3** — *Traslación, Rotación, Escalamiento, Reflexión*
  con la nota de coordenadas homogéneas.
- Di: cada transformación tiene su matriz; la traslación se eleva a coordenadas
  homogéneas 3×3 para poder multiplicarse como las demás (unificar).

### 2.2 Demo de la secuencia (caso del anexo) en la GUI
1. ▶ Rotar, Ángulo **30** → ▶CLIC **«Aplicar»** → pestaña `historial`/`Coordinadas`
   muestra «ÚLTIMA MATRIZ» = `[[0.866,-0.5],[0.5,0.866]]`, figura rota.
2. ▶ Escalar sx=1.5, sy=1.5 → **«Aplicar»** → `[[1.5,0],[0,1.5]]`, crece.
3. ▶ Trasladar dx=2, dy=1 → **«Aplicar»** → homogénea `[[1,0,2],[0,1,1],[0,0,1]]`.
4. ▶ **«Limpiar transformaciones»** → vuelve el cuadrado.
5. ▶ Reflejar, Eje=**y=x** → **«Aplicar»** → `[[0,1],[1,0]]` (espejo). ▶ limpiar.
6. ▶CLIC **«Secuencia de ejemplo»** (aplica Rotar 30 → Escalar 1.5 → Trasladar
   (2,1) de un clic).
7. ▶CLIC: pestaña **Coordenadas** → coordenadas transformadas finales.
- Di: composición `C = T·S·R`; en vectores columna se aplica primero la matriz
  más cercana al vector; **cambiar el orden cambia el resultado** (verificar con
  `np.allclose`).

> Entrega a Antonio en el minuto 12:00.

---

## BLOQUE 3 — Antonio Mora (12:00 – 14:30) · PPT diapositiva 5

### 3.1 Diapositiva 5 · Interfaz, visualización y documentación
- ▶CLIC: PPT **diapositiva 5** — *Interfaz y visualización* + *Documentación del
  proyecto*.
- Di: Tkinter para la interacción (crear figura, elegir transformación);
  Matplotlib para comparar el original vs la transformada; la doc (README,
  informe, bitácora de IA) evidencia el trabajo colaborativo.

### 3.2 Recorrido del programa (el módulo de Antonio)
- ▶CLIC: volver a la ventana abierta y **recorrerla**: panel de controles,
  los dos gráficos (original azul / transformada naranja) con **misma escala**,
  y el cuaderno de pestañas (Coordenadas / Vectores / Subespacio / Historial).
- ▶CLIC: botón **«Guardar gráfico PNG»** → elegir nombre → se guarda la comparación.
- ▶CLIC: abrir `README.md` y `docs/` (informe técnico y bitácora grupal).

---

## BLOQUE 4 — Marcos Gutiérrez (14:30 – 17:00) · PPT diapositivas 4 y 6

### 4.1 Historial y Matriz Compuesta · **PPT diapositiva 4**
- ▶CLIC: PPT **diapositiva 4** — *Registro de operaciones* y *Matriz compuesta
  homogénea* (`C = T·S·R`; se aplica R → S → T).
- Di: cada transformación se registra (nombre, matriz, estado antes / la), lo que
  permite auditar, deshacer y reconstruir el estado final con la matriz compuesta.
- ▶CLIC: pestaña **Historial** en la GUI → recorrer los 3 registros y la
  **MATRIZ COMPUESTA** homogénea.

### 4.2 Resultados, IA y Conclusiones · **PPT diapositiva 6**
- ▶CLIC: PPT **diapositiva 6** — *Pruebas y validación*, *Uso responsable de IA*,
  *Conclusión*.
- ▶CLIC (IA): abrir `docs/bitacoras/*.txt` y la `docs/Bitacora_IA_Grupal.pdf`.
- Di: qué herramienta usaron (ajustar el nombre real) y **cómo la validaron**:
  revisar cada matriz contra la teoría, ejecutar `unittest`, verificación
  numérica manual de rotación/reflexión/composición.
- Di (conclusión): aprendizajes (componer con matrices homogéneas, orden de la
  composición, distinguir conjunto finito vs el espacio que genera); dificultades;
  mejoras (deshacer/rehacer, otras transformaciones, exportar LaTeX); cierre
  invitando a las preguntas.

---

## Respuestas sugeridas a las preguntas de la calificación (repaso)

- **¿Por qué una rotación se representa con una matriz?** Porque es una
  transformación lineal (respeta suma y producto por escalar) sobre vectores
  columna; la matriz concentra la acción y permite componer.
- **¿Qué sucede si cambia el orden?** La composición no conmuta: cambia `C` y
  con él el resultado gráfico.
- **¿Cómo implementaron la multiplicación de matrices?** Con el operador `@` de
 NumPy; para la secuencia componen `C = T·S·R` pasando a coordenadas 3×3 homogéneas.
- **¿Cómo verifican la independencia lineal?** Gauss–Jordan propio: rango de la
  matriz igual al número de vectores → independientes.
- **¿Cómo determinan una base?** Eligen vectores del conjunto cuya agregación
  incrementa el rango (`_indices_base`).
- **¿Cómo detectan información redundante?** Índices que no entran en la base
  (no incrementan el rango).
- **¿Qué ventaja tiene el historial?** Guarda nombre / matriz / estado
  anterior/posterior y permite reconstruir el resultado final con la matriz
  compuesta.
- **¿Cómo validaron el uso de IA?** Comparando matrices contra la teoría,
  ejecutando las pruebas y revisando el código y los resultados manualmente.

---

## Checklist antes de grabar
- [ ] Interfaz cargada con una figura; `python src/interfaz.py --demo` listo por
      si falla la ventana.
- [ ] El PowerPoint abierto y cada uno identifica sus diapositivas (1-6).
- [ ] Cada uno conoce su bloque y su límite de minutos.
- [ ] Misma escala en los dos gráficos (ya configurado en la interfaz).
- [ ] Bitácoras de IA e informe descargados.
- [ ] Micrófono y ensayo de un bloque completo.