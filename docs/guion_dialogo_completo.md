# GUIÓN COMPLETO DE DIÁLOGO — Video PixelForge MathEngine 2D v1.0

> Equipo (orden): **Jose**, **Alejandro**, **Antonio**, **Marcos**. Total ~17 min.
> Regla: hablar siempre sobre el programa corriendo; la diapositiva se muestra un
> momento y se vuelve al programa. `[DIA:]` = qué está en pantalla, `[CLIC:]` = qué
> se hace. **Las líneas entre comillas (« ») son el texto que se dice en voz alta.**

---

# BLOQUE 1 — JOSE (0:00 – 8:30) · Diapositivas 1 y 2

**[DIA: PPT diapositiva 1 — portada «PixelForge MathEngine 2D v1.0» con los cuatro nombres.]**

«Buenos días. Somos el equipo de Álgebra Lineal y hoy les vamos a presentar
nuestro proyecto: se llama **PixelForge Math Engine 2D**, versión 1.0. Es un
proyecto académico del curso FUN-06 de Álgebra Lineal de la Universidad
CENFOTEC.

Quiero aclarar algo desde el inicio: esto **no es un videojuego**. Es un
**motor matemático**, un prototipo, que aplica conceptos de álgebra lineal
para **representar, transformar y visualizar** figuras geométricas en dos
dimensiones usando matrices y vectores. El equipo está integrado por cuatro
personas: yo, Jose, soy el primero en presentar; luego Alejandro, Antonio y
Marcos.»

**[DIA: código abierto en `src/` + diagrama: Objeto2D → Transformador → Historial →
AnalizadorVectorial. CLIC: recorrer los archivos.]**

«Antes de ver la interfaz, les muestro **cómo está organizado el programa**.
La estructura está pensada en módulos, cada uno con una responsabilidad clara.

Tenemos **objetos.py**, que representa las figuras; **transformaciones.py**,
que aplica las transformaciones geométricas; **analisis_vectorial.py**, que
hace el análisis matemático; **historial.py**, que guarda el historial de
operaciones; e **interfaz.py**, que es la ventana que vemos en pantalla. Toda
esa lógica la coordina una clase llamada `Motor2DController`, y la interfaz de
Tkinter es solamente la capa de presentación. Aquí no se repite ninguna de las
cuentas matemáticas.

El flujo general es siempre el mismo: creamos una **figura**, le aplicamos
una **transformación**, esa transformación queda en el **historial** y
finalmente **analizamos** los vectores que resultaron.»

**[DIA: PPT diapositiva 2 «José · Representación y Análisis vectorial».]**

«La base de todo el proyecto es la forma en la que guardamos las figuras.
Cada objeto se representa como una **matriz de dos filas por N columnas**,
donde cada columna es un vértice con su coordenada X y su coordenada Y. Por
ejemplo, un triángulo tendría tres columnas.

¿Por qué vale la pena guardarla como matriz? Porque nos deja aplicar
operaciones lineales sobre toda la figura de una sola vez y también nos
permite analizarla matemáticamente: la independencia lineal nos dice cuántos
vértices son realmente necesarios; si hay vértices redundantes, quiere decir
que algunos son combinación lineal de otros.

Hagamos la demostración. Voy a **ejecutar la interfaz** y crear un cuadrado.»

**[CLIC: `python src/interfaz.py`. DIA: se abre la ventana con el cuadrado azul y
la copia a la derecha. CLIC: Tipo=Cuadrado, Lado=2, Origen 0/0, botón «Crear /
reiniciar figura». CLIC: pestaña Coordenadas.]**

«Aquí tenemos el cuadrado. Se abre en la pestaña de **Coordenadas**. Obsérven
que las coordenadas originales se muestran como una matriz de dos por cuatro.
La primera fila son las X y la segunda las Y. El vértice uno es el de la
esquina (cero, cero), el segundo es el (dos, cero), y así sucesivamente.»

**[CLIC: abrir `objetos.py` y señalar `_convertir_a_matriz` y `clonar()`. CLIC:
abrir `analisis_vectorial.py` y señalar `_gauss_jordan` y `_indices_base`.
CLIC: pestaña Vectores.]**

«En el código, el método `_convertir_a_matriz` se encarga de normalizar el
formato, y `clonar` usa una copia independiente en memoria para no perder la
figura original. El análisis lo hace una **eliminación de Gaus–Jordan** que
nosotros mismos implementamos. La clave es que **no usamos** las funciones
prohibidas de la librería: ni la inversa, ni eigenvalores, ni el rango. Todo
eso lo calculamos con nuestro propio código.

En la pestaña **Vectores** vemos el resultado: la independencia lineal, la
dimensión y la base del espacio generado.»

**[CLIC: pestaña Subespacio; a=1, b=1, c=10; botón «Analizar ax + by = c». Luego c=0.]**

«Una cosa más. En la pestaña **Subespacio** analizamos el conjunto de
posiciones definido por una ecuación `ax + by = c`. Si `c` es distinto de
cero, por ejemplo `x + y = 10`, el programa nos dice que no es un subespacio,
porque es una recta que **no pasa por el origen** y, por lo tanto, no contiene
al vector cero.

Y aquí viene el caso interesante: si cambiamos `c` a cero, la recta ahora sí
pasa por el origen y el programa confirma que **es un subespacio de dimensión
uno**. Esa es justamente la diferencia entre una recta afín y un subespacio
vectorial.

Le doy el turno a Alejandro, que viene con las transformaciones.»

---

# BLOQUE 2 — ALEJANDRO (8:30 – 12:00) · Diapositiva 3

**[DIA: PPT diapositiva 3 «Alejandro · Transformaciones geométricas». CLIC: volver
a la ventana.]**

«Gracias, Jose. Bien, ya que tenemos la figura representada como una matriz,
vamos a ver cómo la movemos con transformaciones geométricas. Aplicamos cuatro:
**traslación, rotación, escalamiento y reflexión**.

Cada una tiene asociada su propia matriz. Lo importante aquí es que la
**traslación** no es una transformación lineal en el plano, así que para poder
representarla igual que las demás, elevamos las coordenadas a un formato
**homogéneo de tres por tres**. Así, toda la operación se puede escibir como
una sola multiplicación de matrices.

Miremos el caso del ejemplo. En la ventana ya tengo el cuadrado.»

**[CLIC: Rotar, Ángulo 30 → botón «Aplicar». CLIC: Escalar sx=1.5 sy=1.5 →
«Aplicar». CLIC: Trasladar dx=2 dy=1 → «Aplicar».]**

«Rodemos el cuadrado treinta grados. La matriz utilizada es la de rotación:
coseno de treinta, menos seno de treinta, arriba; seno de treinta, coseno de
treinta. Vemos que el cuadrado gira alrededor del origen.

Ahora escalamos en uno y cinco en ambos ejes. La matriz es un vector de escala
con uno punto cinco, y la figura crece.

Y por último trasladamos, es decir lo movemos: dos unidades en X y una en Y.
Para eso usamos las coordenadas homogéneas.»

**[CLIC: botón «Limpiar transformaciones». CLIC: Operación Reflejar, Eje y=x,
«Aplicar». CLIC: «Limpiar transformaciones».]**

«También podemos reflejar la figura. Si reflejo respecto a la recta `y = x`, la
matrizes `[cero, uno; uno, cero]` y el cuadrado aparece en espejo sobre esa
diagonal.

Limpiamos y ahora viene lo importante: **aplicar varias transformaciones
consecutivas**. Uso el botón **«Secuencia de ejemplo»**, que hace exactamente
lo que pide el enunciado: rotar treinta grados, escalar en uno punto cinco y
trasladar a dos uno.»

**[CLIC: botón «Secuencia de ejemplo». CLIC: pestaña Historial. CLIC: pestaña
Coordenadas.]**

«La clave de las transformaciones consecutivas está en **componer las matrices
en un solo paso**. La matriz compuesta **C es igual a T por S por R**: la
traslación por la escala por la rotación. Cuiden el orden de la
multiplicación: en los vectores columna se aplica primero la matriz que quedó
más cerca del vector, es decir primero rota, luego escala y al final la
traslación.

Si cambiáramos el orden, por ejemplo trasladar antes de rotar, la matriz
compuesta sería otra y el resultado gráfico sería distinto. Esto lo
verificamos con pruebas numéricas comparando con matrices aproximadas.

Se lo paso a Antonio, que va a mostrar la interfaz.»

---

# BLOQUE 3 — ANTONIO (12:00 – 14:30) · Diapositiva 5

**[DIA: PPT diapositiva 5 «Antonio · Interfaz, Visualización y Documentación».
CLIC: a la ventana.]**

«Gracias, Alejandro. Yo me encargué de la interfaz y de la parte visual.
La interfaz está hecha con **Tkinter** y los gráficos con **Matplotlib**.

La ventana está dividida así. A la izquierda, el panel de **controles**, donde
construimos la figura y elegimos la transformación. Al centro, dos gráficos
cartesianos: la figura original en azul y la transformada en naranja. Es
importante que los dos usan la **misma escala**, para que la comparación sea
lo más honesta posible.

A la derecha tenemos una serie de pestañas: separamos las **matrices y las
coordenadas**, el **análisis vectorial**, el análisis del **subespacujo** y el
**historial**. Así nada queda saturado en una sola pantalla.»

**[CLIC: botón «Guardar gráfico PNG» y elegir nombre. CLIC: abrir `README.md` y
los documentos de `docs/` (informe y bitácula).]**

«Además, el proyecto permite **exportar la comparación como una imagen PNG**,
guardar un gráfico reproducible muy útil para los informes. Y en cuanto a la
**documentación**, dejamos el README con las instrucciones de instalación y uso,
un informe técnico con los fundamentos matemáticos y una bitácula del uso de
inteligencia artificial, como evidencia del trabajo colaborativo.

Leceré a Marcos para el cierre.»

---

# BLOQUE 4 — MARCOS (14:30 – 17:00) · Diapositivas 4 y 6

**[DIA: PPT diapositiva 4 «Marcos · Historial y Matriz Compuesta». CLIC: pestaña
Historial de la ventana.]**

«Muchas gracias. Para cerrar voy a hablar de dos piezas que integran todo: el
**historial** y la **matriz compuesta**.

Cada vez que aplicamos una transformación, el programa la registra guardando el
nombre de la operación, la matriz utilizada y el estado anterior y posterior del
objeto. Eso nos permite auditar el proceso, entender cada paso y también
deshacer, porque conservamos siempre la figura original.

Si nos vamos a la pestaña **Historial** de la ventana, vemos los tres registros
de la secuencia de ejemplo: la rotación, la escala y la traslación. Al final el
programa también nos muestra la **matriz compuesta homogénea**, la que condensa
todas las operaciones en una sola matriz: `C` igual a `T` por `S` por `R`. De
derecha izando a derecha: primero rotación, luego escala y al final traslación.

La utilidad principal es que **con una sola multiplicación reconstruimos el
estado final**, sin repetir los pasos uno por uno.»

**[DIA: PPT diapositiva 6 «Resultados y cierre». CLIC: abrir `docs/bitacoras/*.txt`
y la `Bitacora_IA_Grupal.pdf`.]**

«Y para terminar, sobre el **uso de la inteligencia artificial**. La usamos como
apoyo en todo el proceso, pero lo importante fue ser honestos: toda decisión
técnica y matemática fue discutida, comprendida y validada por el equipo. No
copiamos respuestas a ciegas. Validamos contra la teoría, revisamos cada una de
las matrices y ejecutamos las pruebas automáticas del repositorio.

Las conclusiones:

**Aprendizajes**: componer **matrices homogéneas** y ver el orden en las
transformaciones importa de verdad.

**Dificultades**: precisamente confundirnos con ese orden, que se anota en el
inverso al que se aplica, y también diferenciar un conjunto finito de puntos
del **espacio vectorial** que esos puntos generan.

**Mejoras a futuro**: agregar deshacer y rehacer en el historial, sostener más
transformaciones y exportar las matrices a un formato de Latex.

Como conclusión, **PixelForge** demuestra que los conceptos de Álgebra Lineal
tienen una aplicación real y funcional. Se integran la matemática, la
programación y el trabajo en equipo en un solo motor. Creo que eso es lo más
valioso del proyecto.

Muchas gracias, y quedamos atentos a sus preguntas.»

---

## Notas de cámara (lo que se ve mientras se dice)
- Portada y cierre: mantener la diapositiva del PPT en pantalla.
- En las demostraciones: la ventana del programa enfocada; la diapositiva se
  muestra solo unos segundos y se vuelve al programa.
- Cuando se habla de código, resalten líneas concretas y no dejen un archivo
  abierto por mucho rato.
- En el bloque de Marcos, tener `docs/bitacoras/*.txt` abiertos como evidencia.

### Checklist
- [ ] Programa y PPT abiertos antes de grabar.
- [ ] `python src/interfaz.py --demo` listo como respaldo.
- [ ] Repasar cada bloque con su línea exacta.
- [ ] Micrófono y ensayo completo de un turno.