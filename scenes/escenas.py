from manim import *
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
from utils.comun import *


# =============================================================================
# Utilidades locales de las escenas
# =============================================================================
def fmt(x, dec=2):
    """Numero con coma decimal, listo para usar dentro de MathTex."""
    redondeado = Decimal(str(x)).quantize(Decimal(10) ** -dec, rounding=ROUND_HALF_UP)
    return f"{redondeado:.{dec}f}".replace(".", "{,}")


def mt(*args, **kwargs):
    return MathTex(*args, **kwargs)


def rectangulos_genericos(ejes, g, a, b, n, opacity=0.5):
    """Rectangulos de punto medio para una funcion generica g en [a, b]."""
    dx = (b - a) / n
    grupo = VGroup()
    for i in range(n):
        x0 = a + i * dx
        x1 = x0 + dx
        xm = (x0 + x1) / 2
        h = g(xm)
        color = COL_POS if h >= 0 else COL_NEG
        grupo.add(Polygon(
            ejes.c2p(x0, 0), ejes.c2p(x1, 0),
            ejes.c2p(x1, h), ejes.c2p(x0, h),
            fill_color=color, fill_opacity=opacity,
            stroke_color=color, stroke_width=2,
        ))
    return grupo


def barra_horizontal(x0, x1, y, color, altura=0.62, opacity=0.75):
    """Barra horizontal en coordenadas de pantalla (para el grafico comparativo)."""
    ancho = abs(x1 - x0)
    r = Rectangle(
        width=ancho, height=altura,
        fill_color=color, fill_opacity=opacity,
        stroke_color=color, stroke_width=2.5,
    )
    r.move_to([(x0 + x1) / 2, y, 0])
    return r


# =============================================================================
# ESCENA 1 - PORTADA
# =============================================================================
class Portada(EscenaG6):
    """Presentacion: curso, grupo, integrantes, tema y pregunta central."""

    def construct(self):
        curso = Text("Cálculo Intermedio · MAT1188", font_size=26, color=GREY_A)
        eid = Text("Evaluación Integrada de Desempeño (EID) · 2026",
                   font_size=19, color=GREY_B)
        encabezado = VGroup(curso, eid).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.4)

        grupo = Text(GRUPO, font_size=52, color=GOLD, weight="BOLD")
        integrantes = Text(INTEGRANTES, font_size=23, color=GREY_A, line_spacing=1.0)
        tema = Text("Eje 6 · Integral definida\ny área geométrica",
                    font_size=24, color=WHITE)
        tema2 = Text("Contribuciones positivas\ny negativas",
                     font_size=28, color=COL_CURVA, weight="BOLD")
        col_izq = VGroup(grupo, integrantes, tema, tema2)
        col_izq.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        ajustar(col_izq, 6.4, 3.85)
        col_izq.move_to(LEFT * 3.6 + UP * 0.65)

        ejes = crear_ejes(x_length=5.4, y_length=3.2, numeros=False)
        ejes.move_to(RIGHT * 4.1 + UP * 0.9)
        grafo = grafica(ejes, stroke_width=4.5)
        regiones_mini = regiones(ejes, grafo, opacity=0.55)

        pregunta = cuadro_pregunta(
            "¿Por qué una integral definida puede ser\n"
            "menor que el área geométrica total?"
        )
        pregunta.to_edge(DOWN, buff=0.85)

        self.play(FadeIn(encabezado, shift=DOWN * 0.2))
        self.play(Write(grupo), FadeIn(integrantes, shift=UP * 0.2))
        self.play(Write(tema), Write(tema2))
        self.play(Create(ejes), Create(grafo), FadeIn(regiones_mini), run_time=2)
        self.play(FadeIn(pregunta, scale=0.95))
        self.finalizar()


# =============================================================================
# ESCENA 2 - TEORIA: APORTES CON SIGNO
# =============================================================================

class TeoriaSigno(EscenaG6):
    """Aportes con signo, con pausas para explicar cada elemento de la suma."""

    def construct(self):
        self.play(Write(titulo("El problema: aportes con signo")), run_time=1)
        idea = Text("La altura puede ser positiva o negativa. El ancho es positivo.",
                    font_size=23)
        ajustar(idea, 12.4).to_edge(UP, buff=1.15)
        self.play(FadeIn(idea))

        def g(x):
            return 1.7 * np.sin(1.5 * x)

        ejes = Axes(
            x_range=[-3.6, 3.6, 1], y_range=[-3, 3, 1],
            x_length=8.6, y_length=2.8,
            axis_config={"color": COL_EJE, "stroke_width": 3,
                         "include_ticks": True, "tick_size": 0.06}, tips=False,
        ).shift(UP * 0.2)
        curva = ejes.plot(g, x_range=[-3.2, 3.2], color=COL_CURVA, stroke_width=5)
        suma = mt(r"S_n", "=", r"\sum_{i=1}^{n}",
                  r"f(x_i^*)", r"\,\Delta x").scale(0.95)
        suma[2].set_color(GOLD)
        suma[3].set_color(COL_CURVA)
        suma[4].set_color(YELLOW)
        suma.to_edge(DOWN, buff=1.27)
        condiciones = mt(r"\Delta x=\frac{b-a}{n},\quad a<b,\quad "
                         r"x_i^*\in[x_{i-1},x_i],\quad f\text{ continua}").scale(0.65)
        ajustar(condiciones, 12.4).next_to(suma, DOWN, buff=0.15)

        self.play(Create(ejes), Create(curva), run_time=1.4)
        self.play(Write(suma), FadeIn(condiciones), run_time=1.2)
        rects = rectangulos_genericos(ejes, g, -3.2, 3.2, 10)
        self.play(LaggedStart(*[FadeIn(r) for r in rects], lag_ratio=0.12), run_time=2)

        # Un mismo rectángulo conecta los símbolos con el dibujo.
        x0, x1 = -3.2, -2.56
        xm = (x0 + x1) / 2
        ancho = DoubleArrow(ejes.c2p(x0, -0.35), ejes.c2p(x1, -0.35),
                            buff=0, color=YELLOW,
                            max_tip_length_to_length_ratio=0.18)
        etq_ancho = mt(r"\Delta x", font_size=22, color=YELLOW)
        etq_ancho.next_to(ancho, DOWN, buff=0.08)
        punto = Dot(ejes.c2p(xm, 0), color=GOLD, radius=0.065)
        etq_punto = mt(r"x_i^*", font_size=23, color=GOLD)
        etq_punto.next_to(punto, DOWN, buff=0.18)
        altura = DashedLine(ejes.c2p(xm, 0), ejes.c2p(xm, g(xm)),
                            color=COL_CURVA, stroke_width=5)

        self.esperar_hasta(8.2)
        self.resaltar(suma[4], color=YELLOW,
                      animaciones=(Create(ancho), FadeIn(etq_ancho)))
        self.esperar_hasta(13.2)
        self.resaltar(etq_punto, color=GOLD, run_time=0.6, animaciones=(
            FadeOut(VGroup(ancho, etq_ancho)), FadeIn(punto), FadeIn(etq_punto)))
        self.esperar_hasta(17.2)
        self.resaltar(suma[3], color=COL_CURVA, animaciones=(Create(altura),))
        self.esperar_hasta(19)
        self.resaltar(VGroup(suma[3], suma[4]), color=WHITE)
        self.esperar_hasta(22.8)
        self.play(FadeOut(VGroup(punto, etq_punto, altura)), run_time=0.4)

        etq_pos = Text("aporte positivo", font_size=20, color=COL_POS)
        etq_pos.next_to(ejes.c2p(-2.88, g(-2.88)), UP, buff=0.12)
        etq_neg = Text("aporte negativo", font_size=20, color=COL_NEG)
        etq_neg.move_to(RIGHT * 1.15 + DOWN * 1.1)
        indicador = Arrow(etq_neg.get_top(), ejes.c2p(-0.32, g(-0.32)),
                          buff=0.12, color=COL_NEG, stroke_width=2)
        self.esperar_hasta(24)
        self.resaltar(rects[0], color=COL_POS, animaciones=(FadeIn(etq_pos),))
        self.esperar_hasta(26)
        self.resaltar(rects[4], color=COL_NEG,
                      animaciones=(FadeIn(etq_neg), GrowArrow(indicador)))
        self.esperar_hasta(30)
        self.resaltar(suma, condiciones, color=WHITE)
        self.finalizar()


# =============================================================================
# ESCENA 3 - TEORIA: INTEGRAL vs AREA
# =============================================================================

class TeoriaDefiniciones(EscenaG6):
    """Primero define las áreas y después compara las dos operaciones."""

    def construct(self):
        self.play(Write(titulo("Dos cantidades distintas")), run_time=1)
        a_mas = VGroup(
            mt(r"A^+", color=COL_POS).scale(1.4),
            Text("área de las regiones sobre el eje", font_size=25, color=COL_POS),
        ).arrange(RIGHT, buff=0.4).move_to(UP * 1.4)
        a_menos = VGroup(
            mt(r"A^-", color=COL_NEG).scale(1.4),
            Text("área de las regiones bajo el eje", font_size=25, color=COL_NEG),
        ).arrange(RIGHT, buff=0.4).move_to(DOWN * 0.1)
        nota_areas = Text("Las dos áreas son positivas o cero.", font_size=24)
        nota_areas.move_to(DOWN * 1.5)
        self.play(FadeIn(a_mas), run_time=1.3)
        self.esperar_hasta(4.7)
        self.resaltar(a_mas[0], color=COL_POS)
        self.esperar_hasta(7.1)
        self.play(FadeIn(a_menos))
        self.resaltar(a_menos[0], color=COL_NEG)
        self.esperar_hasta(10.6)
        self.play(FadeIn(nota_areas))
        self.esperar_hasta(17)
        self.quitar_resaltado(run_time=0.8,
                             animaciones=(FadeOut(VGroup(a_mas, a_menos, nota_areas)),))

        integral = mt(r"I=\int_a^b f(x)\,dx=", r"A^+", "-", r"A^-",
                      font_size=46, color=COL_INTEGRAL)
        integral[1].set_color(COL_POS)
        integral[3].set_color(COL_NEG)
        integral_txt = Text("La integral suma los aportes con su signo.",
                            font_size=23, color=COL_INTEGRAL)
        bloque_integral = VGroup(integral, integral_txt).arrange(DOWN, buff=0.25)
        ajustar(bloque_integral, 12).move_to(UP * 1.45)
        area = mt(r"A_{\mathrm{total}}=\int_a^b", r"|f(x)|", r"\,dx=",
                  r"A^+", "+", r"A^-",
                  font_size=43, color=COL_AREA)
        area[3].set_color(COL_POS)
        area[5].set_color(COL_NEG)
        area_txt = Text("El valor absoluto permite sumar todas las áreas.",
                        font_size=23, color=COL_AREA)
        bloque_area = VGroup(area, area_txt).arrange(DOWN, buff=0.25)
        ajustar(bloque_area, 12).move_to(DOWN * 0.65)
        self.play(Write(integral), FadeIn(integral_txt), run_time=1)
        self.esperar_hasta(19.3)
        self.resaltar(integral[2], color=COL_NEG)
        self.esperar_hasta(21)
        self.play(Write(area), FadeIn(area_txt), run_time=2)
        self.esperar_hasta(24)
        self.resaltar(area[4], color=COL_AREA)
        self.esperar_hasta(26.8)
        self.resaltar(area[1], color=COL_AREA, run_time=1.1)
        self.esperar_hasta(32)
        comparacion = mt(r"A^->0\quad\Rightarrow\quad A^+-A^-<A^++A^-", font_size=37)
        comparacion.move_to(DOWN * 2.35)
        nota = Text("Si A⁻ = 0, ambas cantidades coinciden.", font_size=22, color=GREY_A)
        nota.move_to(DOWN * 3.1)
        self.resaltar(comparacion, color=WHITE, run_time=2,
                      animaciones=(Write(comparacion), FadeIn(nota)))
        self.finalizar()


# =============================================================================
# ESCENA 4 - EJEMPLO PRINCIPAL
# =============================================================================
class EjemploPrincipal(EscenaG6):
    """f(x) = x^2 - 4 en [-3, 3]: datos, raices y regiones con signo."""

    def construct(self):
        self.play(Write(titulo("Nuestro ejemplo")), run_time=1)

        datos = VGroup(
            mt(r"f(x) = x^{2} - 4", color=COL_CURVA).scale(1.1),
            Text("intervalo:  [a, b] = [-3, 3]", font_size=21),
            Text("f es un polinomio:\ncontinua en [-3, 3]", font_size=21),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        ajustar(datos, 5.0)
        datos.move_to(LEFT * 4.5 + UP * 1.1)

        ejes = crear_ejes(x_length=7.0, y_length=4.6, shift=RIGHT * 2.2).shift(DOWN * 0.3)
        grafo = grafica(ejes)

        self.play(FadeIn(datos, shift=RIGHT * 0.2))
        self.play(Create(ejes), run_time=1.5)
        self.play(Create(grafo), run_time=2)
        self.esperar_hasta(17)

        # Raices
        raiz_izq = mt(r"x=-2").scale(0.8).next_to(ejes.c2p(-2, -5), DOWN, buff=0.12)
        raiz_der = mt(r"x=2").scale(0.8).next_to(ejes.c2p(2, -5), DOWN, buff=0.12)
        guias_raices = VGroup(*[
            DashedLine(ejes.c2p(x, 0), ejes.c2p(x, -5),
                       color=COL_EJE, stroke_width=1.4, dash_length=0.1)
            for x in RAICES
        ])
        resolucion = mt(r"x^{2} - 4 = 0 \;\Rightarrow\; x = -2 \text{ o } x = 2")
        resolucion.scale(0.8)
        ajustar(resolucion, 4.3)
        resolucion.next_to(datos, DOWN, buff=0.45, aligned_edge=LEFT)

        puntos_raices = VGroup(*[Dot(ejes.c2p(x, 0), radius=0.065, color=GOLD)
                                 for x in RAICES])
        self.play(Create(guias_raices), FadeIn(raiz_izq), FadeIn(raiz_der),
                  FadeIn(puntos_raices))
        self.play(Write(resolucion))
        self.resaltar(raiz_izq, raiz_der, color=GOLD)
        self.esperar_hasta(22.1)

        # Regiones con signo
        regiones_ejem = regiones(ejes, grafo, opacity=0.55)
        etq_pos = Text("f ≥ 0", font_size=22, color=COL_POS).move_to(ejes.c2p(3.55, 2.0))
        etq_neg = mt(r"f < 0", color=COL_NEG).scale(0.75).move_to(ejes.c2p(0.9, -1.2))
        fondo_etq_neg = BackgroundRectangle(etq_neg, fill_opacity=0.85, buff=0.07)

        self.resaltar(regiones_ejem[0], regiones_ejem[2], color=COL_POS,
                      run_time=2, animaciones=(FadeIn(regiones_ejem),))
        self.play(FadeIn(etq_pos), FadeIn(fondo_etq_neg), Write(etq_neg))
        self.esperar_hasta(26.2)
        self.resaltar(regiones_ejem[1], color=COL_NEG)
        self.finalizar()


# =============================================================================
# ESCENA 5 - SUMAS DE RIEMANN CON n = 6
# =============================================================================
class Rectangulos(EscenaG6):
    """Construccion de la suma de Riemann de punto medio con n = 6."""

    def construct(self):
        self.play(Write(titulo("Suma de Riemann con n = 6")), run_time=1)

        n = 6
        ejes = crear_ejes(x_length=7.2, y_length=4.7, shift=LEFT * 2.8).shift(DOWN * 0.35)
        grafo = grafica(ejes)
        self.play(Create(ejes), run_time=1)
        self.play(Create(grafo), run_time=0.8)

        panel = VGroup(
            Text("Partición en 6 subintervalos", font_size=22, color=GOLD),
            mt(r"\Delta x = \frac{3-(-3)}{6} = 1").scale(0.85),
            mt(r"x_i^{*} : \text{ punto medio de cada subintervalo}").scale(0.7),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        ajustar(panel, 5.2)
        panel.move_to(RIGHT * 4.1 + UP * 1.25)
        self.play(FadeIn(panel, shift=DOWN * 0.2), run_time=0.7)
        self.esperar_hasta(3.7)

        guias = guias_verticales(ejes, n)
        self.play(LaggedStart(*[Create(gl) for gl in guias], lag_ratio=0.12),
                  run_time=1)

        puntos = puntos_muestra(ejes, n)
        self.play(LaggedStart(*[GrowFromCenter(p) for p in puntos], lag_ratio=0.15),
                  run_time=1)
        self.esperar_hasta(6)
        self.resaltar(panel[2], puntos, color=GOLD)
        ancho = DoubleArrow(ejes.c2p(2, -0.45), ejes.c2p(3, -0.45),
                            buff=0, color=YELLOW)
        self.esperar_hasta(9)
        self.resaltar(panel[1], color=YELLOW, animaciones=(Create(ancho),))
        self.esperar_hasta(10.5)

        # Rectangulos uno a uno; altura f(x_i*) * dx
        rects = rectangulos_punto_medio(ejes, n)
        self.play(
            LaggedStart(*[FadeIn(r, scale=0.9) for r in rects], lag_ratio=0.35),
            run_time=3.5,
        )

        altura = VGroup(
            Text("altura = f(x_i*)", font_size=21, color=YELLOW),
            Text("aporte = f(x_i*) · Δx", font_size=21, color=YELLOW),
        ).arrange(DOWN, buff=0.18).next_to(panel, DOWN, buff=0.6)
        self.play(FadeIn(altura))
        altura_ejemplo = DashedLine(ejes.c2p(2.5, 0), ejes.c2p(2.5, f(2.5)),
                                    color=COL_CURVA, stroke_width=5)
        self.esperar_hasta(15.4)
        self.resaltar(altura[0], color=COL_CURVA,
                      animaciones=(Create(altura_ejemplo),))

        ejemplo = VGroup(
            mt(r"x^*=2{,}5", font_size=28, color=GOLD),
            mt(r"f(2{,}5)=2{,}5^2-4=2{,}25", font_size=28, color=COL_CURVA),
            mt(r"2{,}25\cdot\Delta x=2{,}25\cdot1=2{,}25",
               font_size=27, color=COL_POS),
        ).arrange(DOWN, buff=0.2)
        ajustar(ejemplo, 5.2).move_to(RIGHT * 4.1 + DOWN * 2.15)
        self.esperar_hasta(20)
        self.play(FadeIn(ejemplo[0]),
                  rects[5].animate.set_stroke(YELLOW, width=5).set_fill(opacity=0.7),
                  run_time=0.5)
        self.resaltar(ejemplo[1], color=COL_CURVA, run_time=0.5,
                      animaciones=(FadeIn(ejemplo[1]),))
        self.esperar_hasta(26)
        self.resaltar(altura[1], ejemplo[2], color=COL_POS,
                      animaciones=(FadeIn(ejemplo[2]),))
        self.finalizar()


# =============================================================================
# ESCENA 6 - SUMA DE LOS APORTES
# =============================================================================
class SumaDeAportes(EscenaG6):
    """Con n = 6: suma de aportes positivos, negativos, integral y area aprox."""

    def construct(self):
        self.play(Write(titulo("Suma de los aportes (n = 6)")), run_time=1)

        n = 6
        ejes = crear_ejes(x_length=6.6, y_length=4.4, shift=LEFT * 3.3).shift(DOWN * 0.5)
        grafo = grafica(ejes)
        rects = rectangulos_punto_medio(ejes, n)
        self.add(ejes, grafo, rects)

        # Panel de resultados a la derecha
        linea1 = mt(r"\sum^{+}=", r"2{,}25", "+", r"2{,}25", "=", r"4{,}5",
                    color=COL_POS).scale(0.85)
        linea2 = VGroup(
            mt(r"\sum^{-}=", r"-1{,}75", r"-3{,}75", font_size=36, color=COL_NEG),
            mt(r"\phantom{\sum^{-}=}", r"-3{,}75", r"-1{,}75", "=-11",
               font_size=36, color=COL_NEG),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        linea3 = mt(r"S_6 = 4{,}5 - 11 = -6{,}5", color=COL_INTEGRAL).scale(0.95)
        linea4 = VGroup(
            Text("Área aproximada:", font_size=21, color=COL_AREA),
            mt(r"4{,}5 + 11 = 15{,}5", color=COL_AREA).scale(0.95),
        ).arrange(RIGHT, buff=0.25)

        panel = VGroup(linea1, linea2, linea3, linea4)
        panel.arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        ajustar(panel, 5.8)
        panel.move_to(RIGHT * 3.75 + UP * 0.6)

        self.play(FadeIn(linea1, shift=RIGHT * 0.2))
        self.esperar_hasta(5.2)
        self.resaltar(rects[0], rects[5], linea1[1], linea1[3], color=COL_POS)
        self.esperar_hasta(11.5)
        self.resaltar(linea1[5], color=COL_POS)
        self.esperar_hasta(14.2)
        self.resaltar(linea2, color=COL_NEG, run_time=1,
                      animaciones=(FadeIn(linea2, shift=RIGHT * 0.2),))
        for segundo, rectangulo, termino in (
            (17, rects[1], linea2[0][1]),
            (20, rects[2], linea2[0][2]),
            (22.6, rects[3], linea2[1][1]),
            (25.7, rects[4], linea2[1][2]),
        ):
            self.esperar_hasta(segundo)
            self.resaltar(rectangulo, termino, color=COL_NEG)
        self.esperar_hasta(31.1)
        self.resaltar(linea2[1][3], color=COL_NEG)
        self.esperar_hasta(33.35)
        self.resaltar(linea3, color=COL_INTEGRAL, run_time=1,
                      animaciones=(FadeIn(linea3, shift=RIGHT * 0.2),))
        self.esperar_hasta(39.85)
        self.resaltar(linea4, color=COL_AREA, run_time=1,
                      animaciones=(FadeIn(linea4, shift=RIGHT * 0.2),))
        self.esperar_hasta(45.85)

        mensaje = Text(
            "La misma partición entrega\ndos números distintos:\n"
            "la suma con signo y la suma de magnitudes.",
            font_size=21, color=GREY_A, line_spacing=1.1,
        )
        ajustar(mensaje, 5.8)
        mensaje.move_to(RIGHT * 3.75 + DOWN * 2.55)
        self.resaltar(linea3, linea4, color=WHITE, run_time=1,
                      animaciones=(FadeIn(mensaje, shift=UP * 0.15),))
        self.finalizar()


# =============================================================================
# ESCENA 7 - REFINAMIENTO DE LA PARTICION
# =============================================================================
class Refinamiento(EscenaG6):
    """n = 6 -> 12 -> 24: la suma con signo tiende a -6 y el area a 46/3."""

    def construct(self):
        self.play(Write(titulo("Refinar la partición:  n → ∞")), run_time=1)

        ejes = crear_ejes(x_length=6.6, y_length=4.5, shift=LEFT * 3.3).shift(DOWN * 0.4)
        grafo = grafica(ejes)
        self.add(ejes, grafo)

        r6 = rectangulos_punto_medio(ejes, 6)
        contador = mt(r"n = 6").scale(1.1).next_to(ejes, UP, buff=0.35)
        self.play(FadeIn(r6), Write(contador), run_time=1.5)

        # Tabla de resultados (columnas fijas para que no se superpongan)
        cols = [1.4, 3.4, 5.55]

        def fila(elementos, y):
            g = VGroup(*elementos)
            for e, x in zip(g, cols):
                e.move_to([x, y, 0])
            return g

        cabeza = fila([
            Text("n", font_size=22, color=GOLD),
            mt(r"S_n", color=COL_INTEGRAL).scale(0.85),
            mt(r"\text{\'Area}_n", color=COL_AREA).scale(0.85),
        ], 2.3)
        def fila_aproximacion(n, y):
            _, _, firmado, area = sumas_punto_medio(n)
            return fila([mt(str(n)).scale(0.9),
                         mt(fmt(firmado), color=COL_INTEGRAL).scale(0.9),
                         mt(fmt(area), color=COL_AREA).scale(0.9)], y)

        fila6 = fila_aproximacion(6, 1.4)
        fila12 = fila_aproximacion(12, 0.6)
        fila24 = fila_aproximacion(24, -0.2)
        limite = fila([mt(r"n\to\infty").scale(0.75), mt("-6", color=COL_INTEGRAL).scale(0.95),
                       mt(r"46/3").scale(0.9).set_color(COL_AREA)], -1.2)
        nota_limite = Text("Valores límite: Δx → 0", font_size=20, color=GREY_A)
        nota_limite.move_to(RIGHT * 3.6 + DOWN * 2.05)
        ajustar(nota_limite, 5.5)

        self.play(FadeIn(cabeza), FadeIn(fila6))
        self.esperar_hasta(7.1)

        # n = 12
        r12 = rectangulos_punto_medio(ejes, 12)
        self.play(
            ReplacementTransform(r6, r12),
            Transform(contador, mt(r"n = 12").scale(1.1).next_to(ejes, UP, buff=0.35)),
            FadeIn(fila12),
            run_time=2.5,
        )
        self.resaltar(fila12, color=GOLD)
        self.esperar_hasta(10.5)

        # n = 24
        r24 = rectangulos_punto_medio(ejes, 24)
        self.play(
            ReplacementTransform(r12, r24),
            Transform(contador, mt(r"n = 24").scale(1.1).next_to(ejes, UP, buff=0.35)),
            FadeIn(fila24),
            run_time=2.5,
        )
        self.resaltar(fila24, color=GOLD)
        self.esperar_hasta(14)

        self.resaltar(limite, color=GOLD, run_time=1,
                      animaciones=(FadeIn(limite, shift=UP * 0.15), FadeIn(nota_limite)))
        self.resaltar(limite[1], color=COL_INTEGRAL, run_time=0.6)
        self.esperar_hasta(17.1)
        self.resaltar(limite[2], color=COL_AREA)
        self.esperar_hasta(21.2)
        self.resaltar(limite[0], nota_limite, color=GOLD)
        self.finalizar()


# =============================================================================
# ESCENA 8 - COMPARACION FINAL CON BARRAS
# =============================================================================

class ComparacionFinal(EscenaG6):
    """Calcula las tres regiones antes de comparar la integral con el área."""

    def construct(self):
        self.play(Write(titulo("Valores exactos: integral y área")), run_time=1)
        primitiva = mt(r"F(x)=\frac{x^3}{3}-4x,", r"\qquad", r"F'(x)=x^2-4", font_size=42)
        primitiva.move_to(UP * 2.1)
        descripcion = Text("Una función cuya derivada es f(x).", font_size=23, color=GREY_A)
        descripcion.move_to(UP * 1.15)
        self.play(Write(primitiva), FadeIn(descripcion), run_time=2)
        self.esperar_hasta(4.5)
        self.resaltar(primitiva[2], color=COL_CURVA)
        self.esperar_hasta(8.8)
        self.resaltar(primitiva[0], color=GOLD)

        izq = mt(r"\int_{-3}^{-2}(x^2-4)\,dx=[F(x)]_{-3}^{-2}=\frac{7}{3}",
                 font_size=37, color=COL_POS).move_to(UP * 0.05)
        der = mt(r"\int_2^3(x^2-4)\,dx=[F(x)]_2^3=\frac{7}{3}",
                 font_size=37, color=COL_POS).move_to(DOWN * 1.15)
        positivo = mt(r"A^+=\frac{7}{3}+\frac{7}{3}=\frac{14}{3}",
                      font_size=40, color=COL_POS).move_to(DOWN * 2.55)
        self.esperar_hasta(19)
        self.resaltar(izq, color=COL_POS, run_time=1, animaciones=(Write(izq),))
        self.resaltar(izq, der, color=COL_POS, run_time=1, animaciones=(Write(der),))
        self.esperar_hasta(23.1)
        self.resaltar(positivo, color=COL_POS, run_time=1, animaciones=(Write(positivo),))
        self.esperar_hasta(25.5)
        self.quitar_resaltado(run_time=0.4,
                             animaciones=(FadeOut(VGroup(izq, der, positivo)),))
        central = mt(r"\int_{-2}^{2}(x^2-4)\,dx=[F(x)]_{-2}^{2}=-\frac{32}{3}",
                     font_size=40, color=COL_NEG).move_to(UP * 0.05)
        negativo = mt(r"A^-=\left|-\frac{32}{3}\right|=\frac{32}{3}",
                      font_size=43, color=COL_NEG).move_to(DOWN * 1.45)
        nota = Text("El área se toma sin signo.", font_size=23, color=GREY_A)
        nota.move_to(DOWN * 2.6)
        self.play(Write(central), run_time=0.7)
        self.resaltar(negativo, color=COL_NEG, run_time=0.7,
                      animaciones=(Write(negativo), FadeIn(nota)))
        self.esperar_hasta(32.2)
        self.quitar_resaltado(run_time=0.4,
                             animaciones=(FadeOut(VGroup(primitiva, descripcion, central, negativo, nota)),))

        s = 0.36
        ancho_pos = A_MAS * s
        ancho_area = AREA_TOTAL * s
        x_neto = INTEGRAL * s
        linea_base = Line([-4.5, -1.8, 0], [6, -1.8, 0], color=COL_EJE, stroke_width=2)
        origen = DashedLine([0, -1.95, 0], [0, 1.55, 0], color=COL_EJE)
        cero = mt("0", font_size=24).move_to([0.22, -1.55, 0])
        integral = mt(r"I=\frac{14}{3}-\frac{32}{3}=-6", font_size=43, color=COL_INTEGRAL)
        integral.move_to(DOWN * 2.6)
        avance = Arrow([0, -0.35, 0], [ancho_pos, -0.35, 0], buff=0, color=COL_POS)
        retroceso = Arrow([ancho_pos, -1.15, 0], [x_neto, -1.15, 0], buff=0, color=COL_NEG)
        enlace = DashedLine([ancho_pos, -0.35, 0], [ancho_pos, -1.15, 0], color=COL_EJE)
        etq_avance = mt(r"+A^+", font_size=27, color=COL_POS).next_to(avance, UP, buff=0.1)
        etq_retroceso = mt(r"-A^-", font_size=27, color=COL_NEG).next_to(retroceso, UP, buff=0.1)
        neto = Dot([x_neto, -1.8, 0], color=COL_INTEGRAL, radius=0.09)
        marca = DashedLine([x_neto, -1.15, 0], [x_neto, -1.8, 0], color=COL_INTEGRAL)
        etq_neto = mt("-6", font_size=27, color=COL_INTEGRAL).move_to([x_neto - 0.4, -1.55, 0])
        self.play(Create(linea_base), Create(origen), Write(cero), run_time=0.6)
        self.resaltar(integral, color=COL_INTEGRAL, run_time=0.8, animaciones=(Write(integral),))
        self.play(GrowArrow(avance), FadeIn(etq_avance), run_time=0.6)
        self.play(Create(enlace), GrowArrow(retroceso), FadeIn(etq_retroceso), run_time=0.8)
        self.play(GrowFromCenter(neto), Create(marca), FadeIn(etq_neto), run_time=0.4)
        self.esperar_hasta(36.7)

        area = mt(r"A_{\mathrm{total}}=\frac{14}{3}+\frac{32}{3}=\frac{46}{3}\approx15{,}33",
                  font_size=39, color=COL_AREA).move_to(UP * 2.5)
        barra_pos = barra_horizontal(0, ancho_pos, 1.15, COL_POS)
        barra_neg = barra_horizontal(ancho_pos, ancho_area, 1.15, COL_NEG)
        etq_pos = mt(r"A^+=14/3", font_size=27, color=COL_POS).next_to(barra_pos, UP, buff=0.16)
        etq_neg = mt(r"A^-=32/3", font_size=27, color=COL_NEG).next_to(barra_neg, UP, buff=0.16)
        self.resaltar(area, color=COL_AREA, run_time=0.7, animaciones=(Write(area),))
        self.play(FadeIn(barra_pos), FadeIn(barra_neg), FadeIn(etq_pos), FadeIn(etq_neg), run_time=0.7)
        self.esperar_hasta(41.4)
        conclusion = mt(r"A^->0\quad\Rightarrow\quad A^+-A^-<A^++A^-", font_size=35)
        conclusion.move_to(DOWN * 3.4)
        self.resaltar(conclusion, color=WHITE, run_time=0.7, animaciones=(Write(conclusion),))
        self.finalizar()


# =============================================================================
# ESCENA 9 - RESPUESTA A LA PREGUNTA CENTRAL
# =============================================================================
class RespuestaCentral(EscenaG6):
    """Respuesta explicita y conexion con el concepto de integral."""

    def construct(self):
        pregunta = cuadro_pregunta(
            "¿Por qué una integral definida puede ser\n"
            "menor que el área geométrica total?"
        )
        pregunta.to_edge(UP, buff=0.4)
        self.play(FadeIn(pregunta, scale=0.95), run_time=0.6)

        respuestas = VGroup(
            Text("Porque la integral suma contribuciones con signo:",
                 font_size=25, color=WHITE),
            Text("las regiones bajo el eje restan.", font_size=25, color=COL_NEG),
            Text("El área geométrica, en cambio, suma todas las magnitudes.",
                 font_size=25, color=COL_AREA),
        ).arrange(DOWN, buff=0.28)
        ajustar(respuestas, 12.4)
        respuestas.move_to(UP * 0.35)
        for segundo, r in zip((0.8, 1.6, 4.3), respuestas):
            self.esperar_hasta(segundo)
            self.resaltar(r, color=r.get_color(), run_time=0.6,
                          animaciones=(FadeIn(r, shift=RIGHT * 0.2),))

        clave = mt(r"A^{+}-A^{-}", "<", r"A^{+}+A^{-}", r"\quad(A^{-}>0)")
        clave.scale(0.95).next_to(respuestas, DOWN, buff=0.55)
        self.esperar_hasta(8.6)
        self.resaltar(clave[3], color=GOLD, run_time=1, animaciones=(Write(clave),))

        cierre = Text(
            "En nuestro ejemplo:  −6  <  15,33   →   la integral es menor.",
            font_size=24, color=GOLD,
        )
        ajustar(cierre, 12.4)
        cierre.to_edge(DOWN, buff=1.5)
        self.esperar_hasta(11.8)
        self.resaltar(cierre, color=GOLD, run_time=0.7,
                      animaciones=(FadeIn(cierre, shift=UP * 0.2),))

        final = Text(
            "Si A⁻ = 0, ambas cantidades coinciden.\n"
            "La integral es el límite de sumas con signo.",
            font_size=21, color=GREY_A, line_spacing=1.15,
        ).to_edge(DOWN, buff=0.6)
        self.esperar_hasta(13.2)
        self.resaltar(final, color=WHITE, run_time=0.8,
                      animaciones=(FadeIn(final, shift=UP * 0.15),))
        self.finalizar()


# =============================================================================
# ESCENA 10 - CREDITOS
# =============================================================================

class Creditos(EscenaG6):
    """Referencias y uso de IA, con el detalle completo en la ficha de entrega."""

    def construct(self):
        self.play(Write(titulo("Fuentes y recursos")), run_time=1)
        fuentes = VGroup(
            Text("Apunte: Introducción a la integral. MAT1188, 2026. Blackboard.", font_size=21, color=GREY_A),
            Text("Stewart. Cálculo de una variable. 7ª ed. Cengage, 2012.", font_size=21, color=GREY_A),
            Text("Thomas, Weir y Hass. Cálculo. Una variable. 12ª ed. Pearson, 2010.", font_size=21, color=GREY_A),
            Text("Manim Community 0.22.0: docs.manim.community", font_size=21, color=GREY_A),
            Text("FFmpeg: recortes de voz, volumen y montaje. ffmpeg.org", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        ajustar(fuentes, 12.4).move_to(UP * 1.2)
        ia = Text(
            "Claude (Anthropic): guía y borrador inicial del código.\n"
            "Codex (OpenAI): revisión de código, guion, ficha, pruebas y montaje.\n"
            "Whisper (OpenAI): transcripción para localizar tomas y recortes.\n"
            "Comprobación: cálculos exactos, pruebas y revisión visual.\n"
            "Referencias y declaración completa en la ficha de entrega.",
            font_size=21, color=GREY_A, line_spacing=1.15,
        )
        ajustar(ia, 12.4).move_to(DOWN * 1.3)
        gracias = Text("Gracias.", font_size=32, color=GOLD).move_to(DOWN * 3.0)
        self.play(LaggedStart(*[FadeIn(f) for f in fuentes], lag_ratio=0.2), run_time=1.5)
        self.esperar_hasta(3.5)
        self.play(FadeIn(ia))
        self.esperar_hasta(7.5)
        self.play(Write(gracias), run_time=0.7)
        self.finalizar()
