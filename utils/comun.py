from manim import *
import numpy as np

# =============================================================================
# 1. DATOS DEL EJEMPLO PRINCIPAL
#    Ejemplo propio: f(x) = x^2 - 4 en [-3, 3] (distinto de los del apunte).
# =============================================================================
A, B = -3.0, 3.0              # extremos del intervalo [a, b]
RAICES = (-2.0, 2.0)          # soluciones de x^2 - 4 = 0 dentro de [a, b]


def f(x):
    """Funcion del ejemplo principal: parabola que cruza el eje x dos veces."""
    return x ** 2 - 4


def f_latex():
    """Expresion LaTeX de la funcion (para etiquetas)."""
    return r"f(x) = x^{2} - 4"


# -----------------------------------------------------------------------------
# Valores exactos del ejemplo (caldulos respaldados en el guion):
#
#   Region sobre el eje  A+ = int_{-3}^{-2} f dx + int_{2}^{3} f dx
#                           = 7/3 + 7/3 = 14/3  ~ 4,67
#   Region bajo el eje   A- = int_{-2}^{2} (-f) dx = 32/3  ~ 10,67
#                          (se mide en valor absoluto, siempre positiva)
#
#   Integral definida    int_{-3}^{3} f dx = A+ - A- = 14/3 - 32/3 = -6
#   Area geometrica      Area    = A+ + A- = 14/3 + 32/3 = 46/3 ~ 15,33
#
#   Como A- > 0:  A+ - A- < A+ + A-   =>   integral < area geometrica
# -----------------------------------------------------------------------------
A_MAS = 14 / 3                # contribucion positiva total (A+)
A_MENOS = 32 / 3              # contribucion negativa total (A-, en valor absoluto)
INTEGRAL = A_MAS - A_MENOS    # = -6.0
AREA_TOTAL = A_MAS + A_MENOS  # = 46/3 ~ 15.333


def sumas_punto_medio(n):
    """
    Sumas de Riemann de punto medio con n subintervalos iguales en [A, B].

    Devuelve la tupla (positivo, negativo, firmado, area), donde:
      positivo .. suma de los aportes f(x_i*) * dx  con f(x_i*) >= 0
      negativo .. suma de los aportes f(x_i*) * dx  con f(x_i*) < 0
                  (valor negativo; su valor absoluto es la region bajo el eje)
      firmado ... positivo + negativo  -> aproxima la integral definida
      area ...... positivo - negativo  -> aproxima el area geometrica total

    Nota: para n = 6, 12, 24 los extremos de subintervalo incluyen las
    raices x = -2 y x = 2, por lo que cada rectangulo queda de un solo color.
    """
    dx = (B - A) / n
    positivo = 0.0
    negativo = 0.0
    for i in range(n):
        punto_muestra = A + (i + 0.5) * dx      # punto medio del subintervalo
        aporte = f(punto_muestra) * dx
        if aporte >= 0:
            positivo += aporte
        else:
            negativo += aporte
    firmado = positivo + negativo
    area = positivo - negativo                   # negativo ya es negativo
    return positivo, negativo, firmado, area


# =============================================================================
# 2. ESTILO COMPARTIDO (colores y textos)
# =============================================================================
COL_POS = GREEN_C         # contribuciones positivas / regiones sobre el eje
COL_NEG = RED_C           # contribuciones negativas / regiones bajo el eje
COL_CURVA = BLUE_B        # grafica de f
COL_EJE = GREY_B          # ejes
COL_AREA = YELLOW         # area geometrica total
COL_INTEGRAL = ORANGE     # integral definida
COL_TITULO = GOLD         # titulos de escena
COL_TECNICO = GREY        # notas al pie

GRUPO = "Grupo 6"
LISTA_INTEGRANTES = [
    "Catalina Javiera Vergara Alarcón",
    "Ignacio Alexander De Celis Valencia",
    "Marcelo Fabián Santana Astorga",
]
INTEGRANTES = "\n".join(LISTA_INTEGRANTES)   # una línea por persona (evita desbordes)
PIE_DE_PAGINA = f"{GRUPO} · MAT1188 Cálculo Intermedio · EID 2026"


def titulo(texto, color=COL_TITULO):
    """Titulo de escena, centrado arriba."""
    return Text(texto, font_size=32, color=color).to_edge(UP, buff=0.28)


def subtitulo(texto, color=WHITE, font_size=24):
    """Linea de texto secundaria debajo del titulo."""
    return Text(texto, font_size=font_size, color=color)


def pie(texto=PIE_DE_PAGINA):
    """Pie de pagina discreto con la identificacion del grupo."""
    return Text(texto, font_size=15, color=COL_TECNICO).to_edge(DOWN, buff=0.15)


def cuadro_pregunta(texto, width=9.4, height=1.6):
    """Recuadro destacado para la pregunta central."""
    fondo = RoundedRectangle(
        corner_radius=0.15, width=width, height=height,
        fill_color="#1b3a5c", fill_opacity=0.92, stroke_color=GOLD, stroke_width=3.5,
    )
    texto_mobj = Text(texto, font_size=26, color=YELLOW, line_spacing=1.15)
    texto_mobj.move_to(fondo)
    return VGroup(fondo, texto_mobj)


# =============================================================================
# 3. CONSTRUCTORES VISUALES DEL EJEMPLO
# =============================================================================
def crear_ejes(x_length=10.4, y_length=5.6, shift=ORIGIN, numeros=True):
    """
    Ejes coherentes para todo el proyecto.

    Escala: x de -4 a 4 (enteros) y y de -6 a 6 cada 2 unidades.
    El intervalo [-3, 3] queda con margen a los lados para rotulos.
    Los números de cada marca hacen visible la escala (criterio V4).
    Con numeros=False se omiten para miniaturas (portada).
    """
    ejes = Axes(
        x_range=[-4, 4, 1],
        y_range=[-6, 6, 2],
        x_length=x_length,
        y_length=y_length,
        axis_config={
            "color": COL_EJE,
            "stroke_width": 3.5,
            "include_ticks": True,
            "include_numbers": numeros,
            "font_size": 22,
            "tick_size": 0.07,
        },
        tips=False,
    ).shift(shift)
    etiqueta_x = MathTex("x", font_size=30, color=COL_EJE).next_to(ejes.x_axis, RIGHT)
    etiqueta_y = MathTex("y", font_size=30, color=COL_EJE).next_to(ejes.y_axis, UP)
    ejes.add(etiqueta_x, etiqueta_y)
    return ejes


def grafica(ejes, stroke_width=5):
    """Grafica de f sobre el intervalo completo [A, B]."""
    return ejes.plot(
        f, x_range=[A, B], color=COL_CURVA, stroke_width=stroke_width,
    )


def regiones(ejes, graph, opacity=0.5):
    """
    Sombrea las tres regiones entre la curva y el eje x:
      [ -3, -2] y [2, 3] sobre el eje  -> verde  (contribuciones positivas)
      [ -2, 2]       bajo el eje       -> rojo   (contribuciones negativas)
    """
    r1 = ejes.get_area(graph, x_range=[A, -2], color=COL_POS, opacity=opacity)
    r2 = ejes.get_area(graph, x_range=[-2, 2], color=COL_NEG, opacity=opacity)
    r3 = ejes.get_area(graph, x_range=[2, B], color=COL_POS, opacity=opacity)
    return VGroup(r1, r2, r3)


def puntos_muestra(ejes, n):
    """Puntos muestra x_i* (punto medio de cada subintervalo)."""
    dx = (B - A) / n
    puntos = VGroup()
    for i in range(n):
        xm = A + (i + 0.5) * dx
        puntos.add(Dot(ejes.c2p(xm, f(xm)), radius=0.055, color=YELLOW))
    return puntos


def rectangulos_punto_medio(ejes, n, opacity=0.45):
    """
    Rectangulos de la suma de Riemann de punto medio con n subintervalos.
    Altura de cada rectangulo: f(x_i*) (con signo). Color segun el signo.
    """
    dx = (B - A) / n
    rectangulos = VGroup()
    for i in range(n):
        x0 = A + i * dx
        x1 = x0 + dx
        xm = (x0 + x1) / 2
        altura = f(xm)
        color = COL_POS if altura >= 0 else COL_NEG
        rect = Polygon(
            ejes.c2p(x0, 0),
            ejes.c2p(x1, 0),
            ejes.c2p(x1, altura),
            ejes.c2p(x0, altura),
            fill_color=color,
            fill_opacity=opacity,
            stroke_color=color,
            stroke_width=2.5,
        )
        rectangulos.add(rect)
    return rectangulos


def guias_verticales(ejes, n, color=COL_TECNICO):
    """Lineas punteadas que marcan la particion del intervalo."""
    dx = (B - A) / n
    guias = VGroup()
    for i in range(n + 1):
        xi = A + i * dx
        guias.add(
            DashedLine(
                ejes.c2p(xi, 0), ejes.c2p(xi, -4.6),
                dash_length=0.12, stroke_width=1.5, color=color,
            )
        )
    return guias


# =============================================================================
# 4. AYUDAS ANTI-SUPERPOSICION (ajuste de tamano y revision automatica)
# =============================================================================
ANCHO_SEGURO = 12.4     # el cuadro de Manim mide ~14,2 de ancho; dejamos margen


def ajustar(mobj, ancho=ANCHO_SEGURO, alto=None):
    """Reduce el objeto (sin deformarlo) si es mas ancho/alto que lo indicado.
    Asi ningun texto se sale de la pantalla ni invade otra zona."""
    if mobj.width > ancho:
        mobj.scale_to_fit_width(ancho)
    if alto is not None and mobj.height > alto:
        mobj.scale_to_fit_height(alto)
    return mobj


def _textos(mobj, acumulado):
    """Recorre los objetos y junta los textos (Text / MathTex), sin entrar a los ejes."""
    if isinstance(mobj, (Axes, NumberLine)):
        return
    if isinstance(mobj, (Text, MathTex)):
        acumulado.append(mobj)
        return
    for sub in mobj.submobjects:
        _textos(sub, acumulado)


def revisar(escena):
    """Avisa por consola si dos textos se superponen o si uno se sale de pantalla."""
    textos = []
    for m in escena.mobjects:
        _textos(m, textos)
    nombre = type(escena).__name__
    avisos = getattr(escena, "_avisos", None)
    if avisos is None:
        avisos = escena._avisos = set()

    def caja(m):
        return (m.get_left()[0], m.get_right()[0], m.get_bottom()[1], m.get_top()[1])

    for m in textos:
        if len(m.submobjects) == 0:
            continue
        x0, x1, y0, y1 = caja(m)
        if x0 < -7.1 or x1 > 7.1 or y0 < -4.0 or y1 > 4.0:
            msg = f"[REVISAR] {nombre}: un texto se sale de la pantalla (x {x0:.1f} a {x1:.1f}, y {y0:.1f} a {y1:.1f})"
            if msg not in avisos:
                avisos.add(msg)
                print(msg)
    for i in range(len(textos)):
        for j in range(i + 1, len(textos)):
            a, b = caja(textos[i]), caja(textos[j])
            ancho = min(a[1], b[1]) - max(a[0], b[0])
            alto = min(a[3], b[3]) - max(a[2], b[2])
            if ancho > 0.08 and alto > 0.08:
                msg = (f"[REVISAR] {nombre}: textos superpuestos cerca de "
                       f"x={(max(a[0], b[0]) + min(a[1], b[1])) / 2:.1f}, "
                       f"y={(max(a[2], b[2]) + min(a[3], b[3])) / 2:.1f}")
                if msg not in avisos:
                    avisos.add(msg)
                    print(msg)


class EscenaG6(Scene):
    """Escena base: igual que Scene, pero revisa superposiciones en cada pausa."""

    def wait(self, *args, **kwargs):
        revisar(self)
        super().wait(*args, **kwargs)