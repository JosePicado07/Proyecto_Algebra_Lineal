"""Interfaz gráfica de PixelForge MathEngine 2D.

La lógica que coordina los módulos matemáticos vive en ``Motor2DController``.
Esto permite probar el flujo sin crear una ventana y mantiene a Tkinter como
una capa de presentación.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib
import numpy as np

try:
    from analisis_vectorial import AnalisadorVectorial
    from historial import HistorialTransformaciones, aplicar_y_registrar
    from objetos import (
        Objeto2D,
        crear_cuadrado,
        crear_rectangulo,
        crear_triangulo,
    )
    from transformaciones import Transformador
except ImportError:
    from .analisis_vectorial import AnalisadorVectorial
    from .historial import HistorialTransformaciones, aplicar_y_registrar
    from .objetos import (
        Objeto2D,
        crear_cuadrado,
        crear_rectangulo,
        crear_triangulo,
    )
    from .transformaciones import Transformador


@dataclass(frozen=True)
class ResultadoAnalisis:
    """Resultados listos para mostrar en la interfaz."""

    linealmente_independiente: bool
    base: np.ndarray
    dimension: int
    redundantes: tuple[int, ...]
    cierre_suma: bool
    cierre_escalar: bool
    interpretacion: str


class Motor2DController:
    """Coordina figuras, transformaciones, historial y análisis vectorial."""

    def __init__(self, objeto: Objeto2D | None = None):
        self.transformador = Transformador()
        self.historial = HistorialTransformaciones()
        self.objeto_original = objeto or crear_cuadrado()
        self.objeto_actual = self._copiar_objeto(self.objeto_original)

    @staticmethod
    def _copiar_objeto(objeto: Objeto2D) -> Objeto2D:
        return Objeto2D(objeto.puntos.copy(), nombre=objeto.nombre)

    @staticmethod
    def parsear_puntos(texto: str) -> list[tuple[float, float]]:
        """Convierte ``x,y; x,y; ...`` en una lista validada de puntos."""
        puntos = []
        for numero, fragmento in enumerate(texto.split(";"), start=1):
            fragmento = fragmento.strip()
            if not fragmento:
                continue
            coordenadas = [valor.strip() for valor in fragmento.split(",")]
            if len(coordenadas) != 2:
                raise ValueError(
                    f"El punto {numero} debe tener el formato x,y."
                )
            try:
                puntos.append((float(coordenadas[0]), float(coordenadas[1])))
            except ValueError as exc:
                raise ValueError(
                    f"El punto {numero} contiene una coordenada no numérica."
                ) from exc
        if len(puntos) < 3:
            raise ValueError("Una figura personalizada requiere al menos 3 puntos.")
        return puntos

    def crear_figura(
        self,
        tipo: str,
        *,
        medida_1: float = 2.0,
        medida_2: float = 2.0,
        origen_x: float = 0.0,
        origen_y: float = 0.0,
        puntos: str = "",
    ) -> Objeto2D:
        """Crea una figura y reinicia el historial de transformaciones."""
        clave = tipo.strip().lower()
        origen = (float(origen_x), float(origen_y))
        if clave in {"cuadrado", "square"}:
            if float(medida_1) <= 0:
                raise ValueError("El lado debe ser mayor que cero.")
            objeto = crear_cuadrado(float(medida_1), origen)
        elif clave in {"triángulo", "triangulo", "triangle"}:
            if float(medida_1) <= 0 or float(medida_2) <= 0:
                raise ValueError("La base y la altura deben ser mayores que cero.")
            objeto = crear_triangulo(float(medida_1), float(medida_2), origen)
        elif clave in {"rectángulo", "rectangulo", "rectangle"}:
            if float(medida_1) <= 0 or float(medida_2) <= 0:
                raise ValueError("El ancho y el alto deben ser mayores que cero.")
            objeto = crear_rectangulo(float(medida_1), float(medida_2), origen)
        elif clave in {"personalizada", "personalizado", "custom"}:
            objeto = Objeto2D(self.parsear_puntos(puntos), nombre="Personalizada")
        else:
            raise ValueError(f"Tipo de figura no soportado: {tipo}.")

        self.objeto_original = objeto
        self.objeto_actual = self._copiar_objeto(objeto)
        self.historial.limpiar()
        return self.objeto_actual

    def aplicar_transformacion(self, operacion: str, **parametros: Any) -> Objeto2D:
        """Aplica una operación al estado actual y la registra."""
        clave = operacion.strip().lower()
        anterior = self.objeto_actual

        if clave in {"trasladar", "traslación", "traslacion"}:
            dx = float(parametros.get("dx", 0.0))
            dy = float(parametros.get("dy", 0.0))
            nombre = f"Traslación dx={dx:g}, dy={dy:g}"
            resultado = self.transformador.trasladar(anterior, dx, dy)
        elif clave in {"rotar", "rotación", "rotacion"}:
            angulo = float(parametros.get("angulo", 0.0))
            nombre = f"Rotación {angulo:g}°"
            resultado = self.transformador.rotar(anterior, angulo)
        elif clave in {"escalar", "escalamiento"}:
            sx = float(parametros.get("sx", 1.0))
            sy_valor = parametros.get("sy", sx)
            sy = sx if sy_valor in (None, "") else float(sy_valor)
            nombre = f"Escalamiento sx={sx:g}, sy={sy:g}"
            resultado = self.transformador.escalar(anterior, sx, sy)
        elif clave in {"reflejar", "reflexión", "reflexion"}:
            eje = str(parametros.get("eje", "x"))
            nombre = f"Reflexión respecto a {eje}"
            resultado = self.transformador.reflejar(anterior, eje)
        else:
            raise ValueError(f"Transformación no soportada: {operacion}.")

        self.objeto_actual = aplicar_y_registrar(
            self.historial, nombre, anterior, resultado
        )
        return self.objeto_actual

    def ejecutar_secuencia_demo(self) -> Objeto2D:
        """Reinicia y aplica rotación 30°, escala 1.5 y traslación (2, 1)."""
        self.reiniciar_transformaciones()
        self.aplicar_transformacion("Rotar", angulo=30.0)
        self.aplicar_transformacion("Escalar", sx=1.5, sy=1.5)
        self.aplicar_transformacion("Trasladar", dx=2.0, dy=1.0)
        return self.objeto_actual

    def reiniciar_transformaciones(self) -> Objeto2D:
        self.objeto_actual = self._copiar_objeto(self.objeto_original)
        self.historial.limpiar()
        return self.objeto_actual

    def analizar(self) -> ResultadoAnalisis:
        analizador = AnalisadorVectorial(self.objeto_actual)
        independiente = analizador.es_linealmente_independiente()
        base = analizador.encontrar_base()
        dimension = analizador.calcular_dimension()
        redundantes = tuple(analizador.detectar_redundantes())
        cierre_suma = analizador.verificar_cierre_suma()
        cierre_escalar = analizador.verificar_cierre_escalar()

        if redundantes:
            posiciones = ", ".join(str(indice + 1) for indice in redundantes)
            redundancia = f"Los vértices {posiciones} son redundantes respecto al conjunto."
        else:
            redundancia = "No se detectaron vértices redundantes."
        interpretacion = (
            f"La figura genera un subespacio de dimensión {dimension} en R². "
            f"{redundancia}"
        )
        return ResultadoAnalisis(
            linealmente_independiente=independiente,
            base=base,
            dimension=dimension,
            redundantes=redundantes,
            cierre_suma=cierre_suma,
            cierre_escalar=cierre_escalar,
            interpretacion=interpretacion,
        )


def _puntos_cerrados(objeto: Objeto2D) -> tuple[np.ndarray, np.ndarray]:
    x, y = objeto.obtener_xy()
    return np.append(x, x[0]), np.append(y, y[0])


def dibujar_comparacion(
    figura: Any,
    original: Objeto2D,
    transformado: Objeto2D,
) -> None:
    """Dibuja original y transformado lado a lado en una Figure de Matplotlib."""
    figura.clear()
    ejes = figura.subplots(1, 2)
    configuraciones = (
        (ejes[0], original, "Figura original", "#2563EB"),
        (ejes[1], transformado, "Figura transformada", "#F97316"),
    )
    todos_x = np.concatenate([original.puntos[0], transformado.puntos[0]])
    todos_y = np.concatenate([original.puntos[1], transformado.puntos[1]])
    margen_x = max(float(np.ptp(todos_x)) * 0.18, 1.0)
    margen_y = max(float(np.ptp(todos_y)) * 0.18, 1.0)
    limite_x = (float(todos_x.min() - margen_x), float(todos_x.max() + margen_x))
    limite_y = (float(todos_y.min() - margen_y), float(todos_y.max() + margen_y))

    for eje, objeto, titulo, color in configuraciones:
        x, y = _puntos_cerrados(objeto)
        eje.fill(x, y, color=color, alpha=0.18)
        eje.plot(x, y, color=color, linewidth=2.2, marker="o", markersize=5)
        for indice, (px, py) in enumerate(objeto.to_lista_tuplas(), start=1):
            eje.annotate(
                f"P{indice}",
                (px, py),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=8,
            )
        eje.axhline(0, color="#94A3B8", linewidth=0.8)
        eje.axvline(0, color="#94A3B8", linewidth=0.8)
        eje.grid(True, color="#E2E8F0", linewidth=0.8)
        eje.set_aspect("equal", adjustable="box")
        eje.set_xlim(*limite_x)
        eje.set_ylim(*limite_y)
        eje.set_title(titulo, fontsize=11, fontweight="bold")
        eje.set_xlabel("x")
        eje.set_ylabel("y")
    figura.tight_layout(pad=2.0)


def guardar_comparacion(
    ruta: str | Path,
    original: Objeto2D,
    transformado: Objeto2D,
) -> Path:
    """Exporta un gráfico reproducible sin depender de la ventana Tk."""
    from matplotlib.figure import Figure

    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    figura = Figure(figsize=(10, 4.8), dpi=150)
    dibujar_comparacion(figura, original, transformado)
    figura.savefig(destino, bbox_inches="tight", facecolor="white")
    return destino


class PixelForgeApp:
    """Ventana principal de PixelForge MathEngine 2D."""

    COLOR_FONDO = "#F1F5F9"
    COLOR_PANEL = "#FFFFFF"
    COLOR_PRIMARIO = "#123B6D"
    COLOR_ACENTO = "#F97316"

    def __init__(self, root: Any):
        import tkinter as tk
        from tkinter import ttk

        matplotlib.use("TkAgg")
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure

        self.tk = tk
        self.ttk = ttk
        self.root = root
        self.controlador = Motor2DController()
        self.figura = Figure(figsize=(8.2, 5.2), dpi=100)

        root.title("PixelForge MathEngine 2D v1.0")
        root.geometry("1360x820")
        root.minsize(1120, 720)
        root.configure(bg=self.COLOR_FONDO)

        self._configurar_estilos()
        self._crear_encabezado()
        self._crear_contenido(FigureCanvasTkAgg)
        self._crear_estado()
        self._actualizar_vista("Motor listo. Seleccione una operación.")

    def _configurar_estilos(self) -> None:
        style = self.ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.COLOR_FONDO)
        style.configure("Panel.TFrame", background=self.COLOR_PANEL)
        style.configure(
            "Title.TLabel",
            background=self.COLOR_PRIMARIO,
            foreground="white",
            font=("Segoe UI", 20, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=self.COLOR_PRIMARIO,
            foreground="#DCEBFA",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Section.TLabel",
            background=self.COLOR_PANEL,
            foreground=self.COLOR_PRIMARIO,
            font=("Segoe UI", 11, "bold"),
        )
        style.configure("Panel.TLabel", background=self.COLOR_PANEL)
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

    def _crear_encabezado(self) -> None:
        header = self.tk.Frame(self.root, bg=self.COLOR_PRIMARIO, height=78)
        header.pack(fill="x")
        header.pack_propagate(False)
        textos = self.tk.Frame(header, bg=self.COLOR_PRIMARIO)
        textos.pack(side="left", padx=24, pady=10)
        self.ttk.Label(
            textos, text="PixelForge MathEngine 2D", style="Title.TLabel"
        ).pack(anchor="w")
        self.ttk.Label(
            textos,
            text="Transformaciones, historial y análisis vectorial en una sola vista",
            style="Subtitle.TLabel",
        ).pack(anchor="w")
        self.tk.Label(
            header,
            text="v1.0",
            bg=self.COLOR_ACENTO,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=14,
            pady=5,
        ).pack(side="right", padx=24)

    def _crear_contenido(self, FigureCanvasTkAgg: Any) -> None:
        contenedor = self.ttk.Frame(self.root, padding=14)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=0)
        contenedor.columnconfigure(1, weight=3)
        contenedor.columnconfigure(2, weight=2)
        contenedor.rowconfigure(0, weight=1)

        controles = self.ttk.Frame(
            contenedor, style="Panel.TFrame", padding=(14, 12)
        )
        controles.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self._crear_panel_controles(controles)

        grafico = self.ttk.Frame(
            contenedor, style="Panel.TFrame", padding=(8, 8)
        )
        grafico.grid(row=0, column=1, sticky="nsew", padx=(0, 10))
        grafico.rowconfigure(1, weight=1)
        grafico.columnconfigure(0, weight=1)
        self.ttk.Label(
            grafico, text="Visualización cartesiana", style="Section.TLabel"
        ).grid(row=0, column=0, sticky="w", padx=8, pady=(2, 6))
        self.canvas = FigureCanvasTkAgg(self.figura, master=grafico)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        resultados = self.ttk.Frame(
            contenedor, style="Panel.TFrame", padding=(10, 10)
        )
        resultados.grid(row=0, column=2, sticky="nsew")
        resultados.rowconfigure(0, weight=1)
        resultados.columnconfigure(0, weight=1)
        self._crear_panel_resultados(resultados)

    def _agregar_campo(
        self, padre: Any, fila: int, etiqueta: str, variable: Any, ancho: int = 10
    ) -> None:
        self.ttk.Label(padre, text=etiqueta, style="Panel.TLabel").grid(
            row=fila, column=0, sticky="w", pady=3
        )
        self.ttk.Entry(padre, textvariable=variable, width=ancho).grid(
            row=fila, column=1, sticky="ew", pady=3, padx=(8, 0)
        )

    def _crear_panel_controles(self, padre: Any) -> None:
        padre.columnconfigure(1, weight=1)
        self.tipo_figura = self.tk.StringVar(value="Cuadrado")
        self.medida_1 = self.tk.StringVar(value="2")
        self.medida_2 = self.tk.StringVar(value="2")
        self.origen_x = self.tk.StringVar(value="0")
        self.origen_y = self.tk.StringVar(value="0")
        self.puntos = self.tk.StringVar(value="0,0; 3,0; 2,2; 0,2")
        self.operacion = self.tk.StringVar(value="Rotar")
        self.angulo = self.tk.StringVar(value="45")
        self.sx = self.tk.StringVar(value="1.5")
        self.sy = self.tk.StringVar(value="1.5")
        self.dx = self.tk.StringVar(value="2")
        self.dy = self.tk.StringVar(value="1")
        self.eje = self.tk.StringVar(value="x")

        fila = 0
        self.ttk.Label(
            padre, text="1. Construir figura", style="Section.TLabel"
        ).grid(row=fila, column=0, columnspan=2, sticky="w", pady=(0, 7))
        fila += 1
        self.ttk.Label(padre, text="Tipo", style="Panel.TLabel").grid(
            row=fila, column=0, sticky="w", pady=3
        )
        self.ttk.Combobox(
            padre,
            textvariable=self.tipo_figura,
            values=("Cuadrado", "Triángulo", "Rectángulo", "Personalizada"),
            state="readonly",
            width=16,
        ).grid(row=fila, column=1, sticky="ew", padx=(8, 0), pady=3)
        fila += 1
        self._agregar_campo(padre, fila, "Lado/Base/Ancho", self.medida_1)
        fila += 1
        self._agregar_campo(padre, fila, "Altura", self.medida_2)
        fila += 1
        self._agregar_campo(padre, fila, "Origen x", self.origen_x)
        fila += 1
        self._agregar_campo(padre, fila, "Origen y", self.origen_y)
        fila += 1
        self.ttk.Label(padre, text="Puntos x,y; ...", style="Panel.TLabel").grid(
            row=fila, column=0, sticky="w", pady=3
        )
        self.ttk.Entry(padre, textvariable=self.puntos, width=22).grid(
            row=fila, column=1, sticky="ew", padx=(8, 0), pady=3
        )
        fila += 1
        self.ttk.Button(
            padre,
            text="Crear / reiniciar figura",
            command=self._crear_figura,
            style="Accent.TButton",
        ).grid(row=fila, column=0, columnspan=2, sticky="ew", pady=(7, 15))

        fila += 1
        self.ttk.Separator(padre).grid(
            row=fila, column=0, columnspan=2, sticky="ew", pady=2
        )
        fila += 1
        self.ttk.Label(
            padre, text="2. Aplicar transformación", style="Section.TLabel"
        ).grid(row=fila, column=0, columnspan=2, sticky="w", pady=(8, 7))
        fila += 1
        self.ttk.Label(padre, text="Operación", style="Panel.TLabel").grid(
            row=fila, column=0, sticky="w", pady=3
        )
        self.ttk.Combobox(
            padre,
            textvariable=self.operacion,
            values=("Rotar", "Escalar", "Trasladar", "Reflejar"),
            state="readonly",
            width=16,
        ).grid(row=fila, column=1, sticky="ew", padx=(8, 0), pady=3)
        fila += 1
        self._agregar_campo(padre, fila, "Ángulo (°)", self.angulo)
        fila += 1
        self._agregar_campo(padre, fila, "Escala sx", self.sx)
        fila += 1
        self._agregar_campo(padre, fila, "Escala sy", self.sy)
        fila += 1
        self._agregar_campo(padre, fila, "Traslación dx", self.dx)
        fila += 1
        self._agregar_campo(padre, fila, "Traslación dy", self.dy)
        fila += 1
        self.ttk.Label(padre, text="Eje reflexión", style="Panel.TLabel").grid(
            row=fila, column=0, sticky="w", pady=3
        )
        self.ttk.Combobox(
            padre,
            textvariable=self.eje,
            values=("x", "y", "y=x"),
            state="readonly",
            width=10,
        ).grid(row=fila, column=1, sticky="ew", padx=(8, 0), pady=3)
        fila += 1
        self.ttk.Button(
            padre,
            text="Aplicar",
            command=self._aplicar_transformacion,
            style="Accent.TButton",
        ).grid(row=fila, column=0, columnspan=2, sticky="ew", pady=(7, 4))
        fila += 1
        self.ttk.Button(
            padre, text="Secuencia de ejemplo", command=self._secuencia_demo
        ).grid(row=fila, column=0, columnspan=2, sticky="ew", pady=3)
        fila += 1
        self.ttk.Button(
            padre, text="Limpiar transformaciones", command=self._reiniciar
        ).grid(row=fila, column=0, columnspan=2, sticky="ew", pady=3)
        fila += 1
        self.ttk.Button(
            padre, text="Guardar gráfico PNG", command=self._guardar_grafico
        ).grid(row=fila, column=0, columnspan=2, sticky="ew", pady=3)

    def _crear_panel_resultados(self, padre: Any) -> None:
        from tkinter import scrolledtext

        notebook = self.ttk.Notebook(padre)
        notebook.grid(row=0, column=0, sticky="nsew")
        self.texto_resultado = scrolledtext.ScrolledText(
            notebook, wrap="word", font=("Consolas", 9), padx=10, pady=10
        )
        self.texto_analisis = scrolledtext.ScrolledText(
            notebook, wrap="word", font=("Consolas", 9), padx=10, pady=10
        )
        self.texto_historial = scrolledtext.ScrolledText(
            notebook, wrap="word", font=("Consolas", 9), padx=10, pady=10
        )
        notebook.add(self.texto_resultado, text="Coordenadas")
        notebook.add(self.texto_analisis, text="Análisis")
        notebook.add(self.texto_historial, text="Historial")

    def _crear_estado(self) -> None:
        self.estado = self.tk.StringVar()
        barra = self.tk.Label(
            self.root,
            textvariable=self.estado,
            anchor="w",
            bg="#E2E8F0",
            fg="#334155",
            font=("Segoe UI", 9),
            padx=16,
            pady=6,
        )
        barra.pack(fill="x", side="bottom")

    def _numero(self, variable: Any, nombre: str) -> float:
        try:
            return float(variable.get())
        except ValueError as exc:
            raise ValueError(f"{nombre} debe ser un número.") from exc

    def _crear_figura(self) -> None:
        try:
            self.controlador.crear_figura(
                self.tipo_figura.get(),
                medida_1=self._numero(self.medida_1, "Lado/Base/Ancho"),
                medida_2=self._numero(self.medida_2, "Altura"),
                origen_x=self._numero(self.origen_x, "Origen x"),
                origen_y=self._numero(self.origen_y, "Origen y"),
                puntos=self.puntos.get(),
            )
            self._actualizar_vista(f"{self.tipo_figura.get()} creada correctamente.")
        except (TypeError, ValueError) as exc:
            self._mostrar_error(str(exc))

    def _aplicar_transformacion(self) -> None:
        try:
            parametros = {
                "angulo": self._numero(self.angulo, "Ángulo"),
                "sx": self._numero(self.sx, "Escala sx"),
                "sy": self._numero(self.sy, "Escala sy"),
                "dx": self._numero(self.dx, "Traslación dx"),
                "dy": self._numero(self.dy, "Traslación dy"),
                "eje": self.eje.get(),
            }
            self.controlador.aplicar_transformacion(
                self.operacion.get(), **parametros
            )
            self._actualizar_vista(
                f"{self.operacion.get()} aplicada. "
                f"Historial: {len(self.controlador.historial)} operación(es)."
            )
        except (TypeError, ValueError) as exc:
            self._mostrar_error(str(exc))

    def _secuencia_demo(self) -> None:
        self.controlador.ejecutar_secuencia_demo()
        self._actualizar_vista(
            "Secuencia aplicada: rotación 30° → escala 1.5 → traslación (2, 1)."
        )

    def _reiniciar(self) -> None:
        self.controlador.reiniciar_transformaciones()
        self._actualizar_vista("Transformaciones eliminadas; figura original restaurada.")

    def _guardar_grafico(self) -> None:
        from tkinter import filedialog

        ruta = filedialog.asksaveasfilename(
            title="Guardar comparación",
            defaultextension=".png",
            filetypes=[("Imagen PNG", "*.png")],
            initialfile="comparacion_pixelforge.png",
        )
        if ruta:
            self.figura.savefig(ruta, dpi=180, bbox_inches="tight", facecolor="white")
            self.estado.set(f"Gráfico guardado en {ruta}")

    def _mostrar_error(self, mensaje: str) -> None:
        from tkinter import messagebox

        messagebox.showerror("Dato inválido", mensaje)
        self.estado.set(f"Error: {mensaje}")

    @staticmethod
    def _formatear_matriz(matriz: np.ndarray) -> str:
        return np.array2string(
            np.asarray(matriz),
            precision=4,
            suppress_small=True,
            floatmode="fixed",
        )

    def _escribir(self, widget: Any, texto: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", texto)
        widget.configure(state="disabled")

    def _actualizar_vista(self, mensaje: str) -> None:
        original = self.controlador.objeto_original
        actual = self.controlador.objeto_actual
        dibujar_comparacion(self.figura, original, actual)
        self.canvas.draw_idle()

        texto_coordenadas = (
            "COORDENADAS ORIGINALES (2×N)\n"
            f"{self._formatear_matriz(original.puntos)}\n\n"
            "COORDENADAS TRANSFORMADAS (2×N)\n"
            f"{self._formatear_matriz(actual.puntos)}"
        )
        if self.controlador.historial.registros:
            ultima = self.controlador.historial.registros[-1]
            texto_coordenadas += (
                "\n\nÚLTIMA MATRIZ UTILIZADA\n"
                f"{ultima.nombre}\n{self._formatear_matriz(ultima.matriz)}"
            )
        else:
            texto_coordenadas += "\n\nÚLTIMA MATRIZ UTILIZADA\nSin transformaciones."
        self._escribir(self.texto_resultado, texto_coordenadas)

        analisis = self.controlador.analizar()
        red = (
            ", ".join(str(indice + 1) for indice in analisis.redundantes)
            if analisis.redundantes
            else "Ninguno"
        )
        texto_analisis = (
            "ANÁLISIS VECTORIAL\n\n"
            f"Independencia lineal: {'Sí' if analisis.linealmente_independiente else 'No'}\n"
            f"Dimensión: {analisis.dimension}\n"
            f"Vértices redundantes: {red}\n"
            f"Cierre bajo suma: {'Cumple' if analisis.cierre_suma else 'No cumple'}\n"
            f"Cierre bajo producto escalar: "
            f"{'Cumple' if analisis.cierre_escalar else 'No cumple'}\n\n"
            f"Base encontrada:\n{self._formatear_matriz(analisis.base)}\n\n"
            f"Interpretación geométrica:\n{analisis.interpretacion}"
        )
        self._escribir(self.texto_analisis, texto_analisis)

        if self.controlador.historial.registros:
            bloques = []
            for numero, registro in enumerate(
                self.controlador.historial.registros, start=1
            ):
                bloques.append(
                    f"{numero}. {registro.nombre}\n"
                    f"{self._formatear_matriz(registro.matriz)}"
                )
            bloques.append(
                "MATRIZ COMPUESTA HOMOGÉNEA\n"
                f"{self._formatear_matriz(self.controlador.historial.matriz_compuesta())}"
            )
            texto_historial = "\n\n".join(bloques)
        else:
            texto_historial = "No hay transformaciones registradas."
        self._escribir(self.texto_historial, texto_historial)
        self.estado.set(mensaje)


def ejecutar_demo_cli(ruta_grafico: str | Path | None = None) -> Motor2DController:
    """Ejecuta el caso de la consigna y muestra resultados sin abrir Tkinter."""
    controlador = Motor2DController()
    controlador.ejecutar_secuencia_demo()
    analisis = controlador.analizar()
    print("PIXELFORGE MATHENGINE 2D — DEMOSTRACIÓN")
    print("=" * 56)
    print(f"Figura original:\n{np.round(controlador.objeto_original.puntos, 6)}")
    for numero, registro in enumerate(controlador.historial.registros, start=1):
        print(f"\n{numero}. {registro.nombre}")
        print(np.round(registro.matriz, 6))
    print("\nFigura transformada:")
    print(np.round(controlador.objeto_actual.puntos, 6))
    print("\nMatriz compuesta homogénea:")
    print(np.round(controlador.historial.matriz_compuesta(), 6))
    print(f"\nDimensión: {analisis.dimension}")
    print(f"Base:\n{np.round(analisis.base, 6)}")
    print(f"Índices redundantes: {list(analisis.redundantes)}")
    if ruta_grafico:
        destino = guardar_comparacion(
            ruta_grafico, controlador.objeto_original, controlador.objeto_actual
        )
        print(f"\nGráfico guardado en: {destino}")
    return controlador


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Ejecuta el caso de ejemplo en consola sin abrir la GUI.",
    )
    parser.add_argument(
        "--grafico",
        type=Path,
        help="Ruta PNG para exportar la comparación durante --demo.",
    )
    args = parser.parse_args()

    if args.demo:
        ejecutar_demo_cli(args.grafico)
        return

    import tkinter as tk

    root = tk.Tk()
    PixelForgeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
