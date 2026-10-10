ï»¿from manim import *
from utils.comun import *


# =============================================================================
# Utilidades locales de las escenas
# =============================================================================
def fmt(x, dec=2):
    """Numero con coma decimal, listo para usar dentro de MathTex."""
    return f"{x:.{dec}f}".replace(".", "{,}")


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
class Portada(Scene):
    """Presentacion: curso, grupo, integrantes, tema y pregunta central."""

    def construct(self):
        curso = Text("CÃ¡lculo Intermedio Ã· MAT1188", font_size=26, color=GREY_A)
        eid = Text("Evaluaciónón Integrada de DesempeÃ±o (EID) Ã· 2026",
                   font_size=19, color=GREY_B)
        encabezado = VGroup(curso, eid).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.4)

        grupo = Text(GRUPO, font_size=52, color=GOLD, weight="BOLD")
        integrantes = Text(INTEGRANTES, font_size=21, color=GREY_A)
        tema = Text("Eje 6 Ã· Integral definida y Ã¡rea geomÃ©trica",
                    font_size=25, color=WHITE)
        tema2 = Text("Contribuciones positivas y negativas",
                     font_size=29, color=COL_CURVA, weight="BOLD")
        col_izq = VGroup(grupo, integrantes, tema, tema2)
        col_izq.arrange(DOWN, buff=0.30, aligned_edge=LEFT)
        col_izq.move_to(LEFT * 3.5 + UP * 0.9)

        ejes = crear_ejes(x_length=5.4, y_length=3.2, numeros=False)
        ejes.move_to(RIGHT * 4.1 + UP * 0.9)
        grafo = grafica(ejes, stroke_width=4.5)
        regiones_mini = regiones(ejes, grafo, opacity=0.55)

        pregunta = cuadro_pregunta(
            "Ã¿Por quééÃ© una integral definida puede ser\n"
            "menor que el Ã¡rea geomÃ©trica total?"
        )
        pregunta.to_edge(DOWN, buff=0.85)

        self.play(FadeIn(encabezado, shift=DOWN * 0.2))
        self.play(Write(grupo), FadeIn(integrantes, shift=UP * 0.2))
        self.play(Write(tema), Write(tema2))
        self.play(Create(ejes), Create(grafo), FadeIn(regiones_mini), run_time=2)
        self.play(FadeIn(pregunta, scale=0.95))
        self.wait(3)


# =============================================================================
# ESCENA 2 - TEORIA: APORTES CON SIGNO
# =============================================================================
class TeoriaSigno(Scene):
    """Cuando f toma valores negativos aparecen aportes negativos."""

    def construct(self):
        self.add(pie())
        self.play(Write(titulo("El problema: aportes con signo")))

        idea = Text(
            "Si f toma valores negativos en [a, b], algunos aportes son negativos.",
            font_size=25,
        ).to_edge(UP, buff=1.15)
        self.play(FadeIn(idea, shift=DOWN * 0.2))
        self.wait(2)

        def g(x):
            return 1.7 * np.sin(1.5 * x)

        ejes = Axes(
            x_range=[-3.6, 3.6, 1], y_range=[-3, 3, 1],
            x_length=8.6, y_length=3.3,
            axis_config={"color": COL_EJE, "stroke_width": 3,
                         "include_ticks": True, "tick_size": 0.06},
            tips=False,
        ).shift(DOWN * 0.35)
        curva = ejes.plot(g, x_range=[-3.2, 3.2], color=COL_CURVA, stroke_width=5)
        rects = rectangulos_genericos(ejes, g, -3.2, 3.2, 10)

        self.play(Create(ejes), run_time=1.2)
        self.play(Create(curva), run_time=1.2)
        self.play(
            LaggedStart(*[FadeIn(r, scale=0.9) for r in rects], lag_ratio=0.12),
            run_time=2.5,
        )

        # Etiquetas sobre un rectangulo positivo y uno negativo
        etq_pos = Text("aporte positivo", font_size=20, color=COL_POS)
        etq_pos.next_to(ejes.c2p(-2.88, g(-2.88)), UP, buff=0.12)
        etq_neg = Text("aporte negativo", font_size=20, color=COL_NEG)
        etq_neg.next_to(ejes.c2p(-0.32, g(-0.32)), DOWN, buff=0.12)
        self.play(FadeIn(etq_pos), FadeIn(etq_neg))
        self.wait(2)

        # Formula de la suma de Riemann
        suma = mt(r"S_n = \sum_{i=1}^{n} f(x_i^{*})\,\Delta x").scale(0.95)
        suma.to_edge(DOWN, buff=0.75)
        self.play(Write(suma))
        self.wait(1.5)

        condiciones = mt(
            r"\Delta x = \frac{b-a}{n}, \qquad "
            r"x_i^{*} \in [x_{i-1},\,x_i], \qquad "
            r"f \text{ continua en } [a,b]"
        ).scale(0.7)
        condiciones.next_to(suma, DOWN, buff=0.3)
        self.play(FadeIn(condiciones, shift=UP * 0.15))
        self.wait(2.5)


# =============================================================================
# ESCENA 3 - TEORIA: INTEGRAL vs AREA
# =============================================================================
class TeoriaDefiniciones(Scene):
    """Dos cantidades distintas: integral definida (con signo) y area (magnitudes)."""

    def construct(self):
        self.add(pie())
        self.play(Write(titulo("Dos cantidades distintas")))

        # Contribucion positiva
        a_mas = VGroup(
            mt(r"A^{+}", color=COL_POS).scale(1.5),
            Text("regiones sobre el eje  (f Ã¢â°¥ 0)", font_size=23),
        ).arrange(RIGHT, buff=0.4)
        a_mas[1].set_color(COL_POS)

        # Contribucion negativa
        a_menos = VGroup(
            mt(r"A^{-}", color=COL_NEG).scale(1.5),
            Text("regiones bajo el eje, en valor absoluto  (f < 0)", font_size=23),
        ).arrange(RIGHT, buff=0.4)
        a_menos[1].set_color(COL_NEG)

        self.play(FadeIn(a_mas, shift=RIGHT * 0.3))
        self.wait(1)
        self.play(FadeIn(a_menos, shift=RIGHT * 0.3))
        self.wait(1.5)

        # Integral definida
        integral = mt(r"\int_{a}^{b} f(x)\,dx \;=\; A^{+} - A^{-}",
                      color=COL_INTEGRAL).scale(1.15)
        integral_txt = Text("integral definida: contribuciones con signo",
                            font_size=21, color=COL_INTEGRAL)

        # Area geometrica
        area = mt(r"\text{Area geomÃ©trica} \;=\; A^{+} + A^{-}",
                  color=COL_AREA).scale(1.15)
        area_txt = Text("Ã¡rea geomÃ©trica: todas las magnitudes se suman",
                        font_size=21, color=COL_AREA)

        bloque_integral = VGroup(integral, integral_txt).arrange(DOWN, buff=0.2)
        bloque_area = VGroup(area, area_txt).arrange(DOWN, buff=0.2)

        columnas = VGroup(a_mas, a_menos)
        columnas.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        columnas.to_edge(UP, buff=1.5)

        self.play(FadeOut(columnas))
        self.play(Write(integral), FadeIn(integral_txt, shift=UP * 0.15))
        self.wait(1.5)
        self.play(Write(area), FadeIn(area_txt, shift=UP * 0.15))
        self.wait(1.5)

        # Comparacion y condicion
        comparacion = mt(r"A^{+} - A^{-} \;<\; A^{+} + A^{-}"
                         r"\qquad \text{siempre que } A^{-} > 0")
        comparacion.scale(0.9).to_edge(DOWN, buff=1.0)
        nota = Text("Si f no toma valores negativos, AÃ¢» = 0 y ambas cantidades coinciden.",
                    font_size=21, color=GREY_A).to_edge(DOWN, buff=0.45)

        self.play(Write(comparacion))
        self.wait(1)
        self.play(FadeIn(nota, shift=UP * 0.15))
        self.wait(2)


# =============================================================================
# ESCENA 4 - EJEMPLO PRINCIPAL
# =============================================================================
class EjemploPrincipal(Scene):
    """f(x) = x^2 - 4 en [-3, 3]: datos, raices y regiones con signo."""

    def construct(self):
        self.add(pie())
        self.play(Write(titulo("Nuestro ejemplo")))

        datos = VGroup(
            mt(r"f(x) = x^{2} - 4", color=COL_CURVA).scale(1.1),
            Text("intervalo:  [a, b] = [-3, 3]", font_size=23),
            Text("f es un polinomio: continua en [-3, 3]", font_size=23),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        datos.move_to(LEFT * 4.4 + UP * 1.1)

        ejes = crear_ejes(x_length=7.0, y_length=4.6, shift=RIGHT * 2.2).shift(DOWN * 0.3)
        grafo = grafica(ejes)

        self.play(FadeIn(datos, shift=RIGHT * 0.2))
        self.play(Create(ejes), run_time=1.5)
        self.play(Create(grafo), run_time=2)
        self.wait(1.5)

        # Raices
        raiz_izq = mt(r"x=-2").scale(0.8).next_to(ejes.c2p(-2, 0), LEFT, buff=0.15)
        raiz_der = mt(r"x=2").scale(0.8).next_to(ejes.c2p(2, 0), RIGHT, buff=0.15)
        resolucion = mt(r"x^{2} - 4 = 0 \;\Rightarrow\; x = -2 \text{ o } x = 2")
        resolucion.scale(0.8).next_to(datos, DOWN, buff=0.45, aligned_edge=LEFT)

        self.play(FadeIn(raiz_izq), FadeIn(raiz_der))
        self.play(Write(resolucion))
        self.wait(1.5)

        # Regiones con signo
        regiones_ejem = regiones(ejes, grafo, opacity=0.55)
        etq_pos = Text("f Ã¢â°¥ 0", font_size=22, color=COL_POS).next_to(ejes.c2p(2.5, 2.25), UP)
        etq_neg = mt(r"f < 0", color=COL_NEG).scale(0.9).next_to(ejes.c2p(0, -4), DOWN, buff=0.2)

        self.play(FadeIn(regiones_ejem, run_time=2))
        self.play(FadeIn(etq_pos), Write(etq_neg))
        self.wait(2.5)


# =============================================================================
# ESCENA 5 - SUMAS DE RIEMANN CON n = 6
# =============================================================================
class Rectangulos(Scene):
    """Construccion de la suma de Riemann de punto medio con n = 6."""

    def construct(self):
        self.add(pie())
        self.play(Write(titulo("Suma de Riemann con n = 6")))

        n = 6
        ejes = crear_ejes(x_length=7.2, y_length=4.7, shift=LEFT * 2.8).shift(DOWN * 0.35)
        grafo = grafica(ejes)
        self.play(Create(ejes), run_time=1.3)
        self.play(Create(grafo), run_time=1.5)

        panel = VGroup(
            Text("Partición en 6 subintervalos", font_size=22, color=GOLD),
            mt(r"\Delta x = \frac{3-(-3)}{6} = 1").scale(0.85),
            mt(r"x_i^{*} : \text{ punto medio de cada subintervalo}").scale(0.7),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        panel.move_to(RIGHT * 3.9 + UP * 1.25)
        self.play(FadeIn(panel, shift=DOWN * 0.2))

        guias = guias_verticales(ejes, n)
        self.play(LaggedStart(*[Create(gl) for gl in guias], lag_ratio=0.12),
                  run_time=1.8)

        puntos = puntos_muestra(ejes, n)
        self.play(LaggedStart(*[GrowFromCenter(p) for p in puntos], lag_ratio=0.15),
                  run_time=1.5)
        self.wait(1)

        # Rectangulos uno a uno; altura f(x_i*) * dx
        rects = rectangulos_punto_medio(ejes, n)
        self.play(
            LaggedStart(*[FadeIn(r, scale=0.9) for r in rects], lag_ratio=0.35),
            run_time=4.5,
        )

        altura = VGroup(
            Text("altura = f(x_i*)", font_size=21, color=YELLOW),
            Text("aporte = f(x_i*) Ã· Ãâx", font_size=21, color=YELLOW),
        ).arrange(DOWN, buff=0.18).next_to(panel, DOWN, buff=0.6)
        self.play(FadeIn(altura))
        self.wait(3.5)


# =============================================================================
# ESCENA 6 - SUMA DE LOS APORTES
# =============================================================================
class SumaDeAportes(Scene):
    """Con n = 6: suma de aportes positivos, negativos, integral y area aprox."""

    def construct(self):
        self.add(pie())
        self.play(Write(titulo("Suma de los aportes (n = 6)")))

        n = 6
        ejes = crear_ejes(x_length=6.6, y_length=4.4, shift=LEFT * 3.3).shift(DOWN * 0.5)
        grafo = grafica(ejes)
        rects = rectangulos_punto_medio(ejes, n)
        self.add(ejes, grafo, rects)

        # Panel de resultados a la derecha
        linea1 = mt(r"\sum^{+} = 2{,}25 + 2{,}25 = 4{,}5", color=COL_POS).scale(0.85)
        linea2 = mt(r"\sum^{-} = -1{,}75 - 3{,}75 - 3{,}75 - 1{,}75 = -11",
                    color=COL_NEG).scale(0.72)
        linea3 = mt(r"S_6 = 4{,}5 - 11 = -6{,}5", color=COL_INTEGRAL).scale(0.95)
        linea4 = VGroup(
            Text("Ãrea aproximada:", font_size=21, color=COL_AREA),
            mt(r"4{,}5 + 11 = 15{,}5", color=COL_AREA).scale(0.95),
        ).arrange(RIGHT, buff=0.25)

        panel = VGroup(linea1, linea2, linea3, linea4)
        panel.arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        panel.move_to(RIGHT * 3.45 + UP * 0.4)

        self.play(FadeIn(linea1, shift=RIGHT * 0.2))
        self.wait(2.5)
        self.play(FadeIn(linea2, shift=RIGHT * 0.2))
        self.wait(2.5)
        self.play(FadeIn(linea3, shift=RIGHT * 0.2))
        self.wait(2)
        self.play(FadeIn(linea4, shift=RIGHT * 0.2))
        self.wait(2)

        mensaje = Text(
            "La misma partición entrega dos nÃºmeros distintos:",
            font_size=23, color=GREY_A,
        ).to_edge(DOWN, buff=1.5)
        mensaje2 = Text(
            "la suma con signo  y  la suma de magnitudes.",
            font_size=23, color=GREY_A,
        ).next_to(mensaje, DOWN, buff=0.2)
        self.play(FadeIn(mensaje, shift=UP * 0.15), FadeIn(mensaje2, shift=UP * 0.15))
        self.wait(3)


# =============================================================================
# ESCENA 7 - REFINAMIENTO DE LA PARTICION
# =============================================================================
class Refinamiento(Scene):
    """n = 6 -> 12 -> 24: la suma con signo tiende a -6 y el area a 46/3."""

    def construct(self):
        self.add(pie())
        self.play(Write(titulo("Refinar la partición:  n Ã¢â â Ã¢ËÅ¾")))

        ejes = crear_ejes(x_length=6.6, y_length=4.5, shift=LEFT * 3.3).shift(DOWN * 0.4)
        grafo = grafica(ejes)
        self.add(ejes, grafo)

        r6 = rectangulos_punto_medio(ejes, 6)
        contador = mt(r"n = 6").scale(1.1).next_to(ejes, UP, buff=0.35)
        self.play(FadeIn(r6), Write(contador), run_time=1.5)

        # Tabla de resultados
        cabeza = VGroup(
            Text("n", font_size=22, color=GOLD),
            mt(r"S_n", color=COL_INTEGRAL).scale(0.85),
            mt(r"\text{Area}_n", color=COL_AREA).scale(0.85),
        ).arrange(RIGHT, buff=0.85)
        fila6 = VGroup(
            mt("6").scale(0.9),
            mt("-6{,}5", color=COL_INTEGRAL).scale(0.9),
            mt("15{,}5", color=COL_AREA).scale(0.9),
        ).arrange(RIGHT, buff=0.95)
        fila12 = VGroup(
            mt("12").scale(0.9),
            mt("-6{,}13", color=COL_INTEGRAL).scale(0.9),
            mt("15{,}38", color=COL_AREA).scale(0.9),
        ).arrange(RIGHT, buff=0.95)
        fila24 = VGroup(
            mt("24").scale(0.9),
            mt("-6{,}03", color=COL_INTEGRAL).scale(0.9),
            mt("15{,}34", color=COL_AREA).scale(0.9),
        ).arrange(RIGHT, buff=0.95)
        limite = VGroup(
            mt(r"n \to \infty").scale(0.9),
            mt("-6", color=COL_INTEGRAL).scale(0.95),
            mt(r"46/3 \approx 15{,}33", color=COL_AREA).scale(0.9),
        ).arrange(RIGHT, buff=0.7)

        tabla = VGroup(cabeza, fila6, fila12, fila24, limite)
        tabla.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        tabla.move_to(RIGHT * 3.7 + UP * 0.6)

        self.play(FadeIn(cabeza), FadeIn(fila6))
        self.wait(2)

        # n = 12
        r12 = rectangulos_punto_medio(ejes, 12)
        self.play(
            ReplacementTransform(r6, r12),
            Transform(contador, mt(r"n = 12").scale(1.1).next_to(ejes, UP, buff=0.35)),
            FadeIn(fila12),
            run_time=2.5,
        )
        self.wait(2)

        # n = 24
        r24 = rectangulos_punto_medio(ejes, 24)
        self.play(
            ReplacementTransform(r12, r24),
            Transform(contador, mt(r"n = 24").scale(1.1).next_to(ejes, UP, buff=0.35)),
            FadeIn(fila24),
            run_time=2.5,
        )
        self.wait(2)

        self.play(FadeIn(limite, shift=UP * 0.15))
        self.wait(3)


# =============================================================================
# ESCENA 8 - COMPARACION FINAL CON BARRAS
# =============================================================================
class ComparacionFinal(Scene):
    """Integral = A+ - A-  vs  Area = A+ + A-, con barras a escala."""

    def construct(self):
        self.add(pie())
        self.play(Write(titulo("Integral definida frente al Ã¡rea geomÃ©trica")))

        # Escala: A+ = 14/3, A- = 32/3  ->  unidades de pantalla
        s = 0.36
        ancho_pos = A_MAS * s          # ~1,68
        ancho_neg = A_MENOS * s        # ~3,84
        ancho_area = (A_MAS + A_MENOS) * s     # ~5,52
        ancho_integral = A_MAS * s             # parte positiva de la integral

        linea_base = Line(LEFT * 6.4, RIGHT * 6.4, color=COL_EJE, stroke_width=2)

        # Etiquetas de las formulas
        txt_area = mt(r"\text{Area} = A^{+} + A^{-} = \frac{46}{3} \approx 15{,}33",
                      color=COL_AREA).scale(0.85)
        txt_integral = mt(r"\int_{-3}^{3} f\,dx = A^{+} - A^{-} = -6",
                          color=COL_INTEGRAL).scale(0.85)
        txt_area.next_to(linea_base, UP, buff=0.35).to_edge(UP, buff=1.0).shift(LEFT*2.5)
        txt_integral.to_edge(DOWN, buff=0.8).shift(LEFT*2.0)

        # --- Barra superior: AREA (verde + rojo hacia la derecha) ---
        y_area = 1.15
        barra_pos_area = barra_horizontal(0, ancho_pos, y_area, COL_POS)
        barra_neg_area = barra_horizontal(ancho_pos, ancho_area, y_area, COL_NEG)
        etq_pos_area = mt(r"A^{+}", color=COL_POS).scale(0.8).next_to(barra_pos_area, UP, buff=0.05)
        etq_neg_area = mt(r"A^{-}", color=COL_NEG).scale(0.8).next_to(barra_neg_area, UP, buff=0.05)

        # --- Barra inferior: INTEGRAL (positivo a la derecha, negativo a la izquierda) ---
        y_int = -1.05
        barra_pos_int = barra_horizontal(0, ancho_integral, y_int, COL_POS)
        barra_neg_int = barra_horizontal(-ancho_neg, 0, y_int, COL_NEG)
        neto = Dot([-ancho_neg + ancho_pos, y_int, 0], color=COL_INTEGRAL, radius=0.09)
        marca = DashedLine([-ancho_neg + ancho_pos, y_int - 0.5, 0],
                           [-ancho_neg + ancho_pos, y_int + 0.5, 0], color=COL_INTEGRAL)
        etq_neto = mt(r"\text{valor neto}", color=COL_INTEGRAL).scale(0.7)
        etq_neto.next_to(neto, DOWN, buff=0.35)

        self.play(Create(linea_base))
        self.play(Write(txt_area))
        self.play(FadeIn(barra_pos_area), FadeIn(barra_neg_area), run_time=1.8)
        self.play(FadeIn(etq_pos_area), FadeIn(etq_neg_area))
        self.wait(2)

        self.play(Write(txt_integral))
        self.play(FadeIn(barra_neg_int), FadeIn(barra_pos_int), run_time=1.8)
        self.play(GrowFromCenter(neto), Create(marca), FadeIn(etq_neto))
        self.wait(1.5)

        conclusion = mt(r"A^{-} > 0 \;\Rightarrow\; A^{+} - A^{-} < A^{+} + A^{-}")
        conclusion.scale(0.95).to_edge(UP, buff=1.55)
        self.play(Write(conclusion))
        self.wait(3)


# =============================================================================
# ESCENA 9 - RESPUESTA A LA PREGUNTA CENTRAL
# =============================================================================
class RespuestaCentral(Scene):
    """Respuesta explicita y conexion con el concepto de integral."""

    def construct(self):
        self.add(pie())
        pregunta = cuadro_pregunta(
            "Ã¿Por quééÃ© una integral definida puede ser\n"
            "menor que el Ã¡rea geomÃ©trica total?"
        )
        pregunta.to_edge(UP, buff=0.4)
        self.play(FadeIn(pregunta, scale=0.95))
        self.wait(1.5)

        respuestas = VGroup(
            Text("Porque la integral suma contribuciones con signo:",
                 font_size=25, color=WHITE),
            Text("las regiones bajo el eje restan.", font_size=25, color=COL_NEG),
            Text("El Ã¡rea geomÃ©trica, en cambio, suma todas las magnitudes.",
                 font_size=25, color=COL_AREA),
        ).arrange(DOWN, buff=0.28)
        respuestas.move_to(UP * 0.35)
        for i, r in enumerate(respuestas):
            self.play(FadeIn(r, shift=RIGHT * 0.2))
            self.wait(1.2)

        clave = mt(r"A^{+} - A^{-} < A^{+} + A^{-} \quad (A^{-} > 0)")
        clave.scale(0.95).next_to(respuestas, DOWN, buff=0.55)
        self.play(Write(clave))
        self.wait(1.5)

        cierre = Text(
            "En nuestro ejemplo:  Ã¢Ëâ6  <  15,33   Ã¢â â   la integral es menor.",
            font_size=25, color=GOLD,
        ).to_edge(DOWN, buff=1.4)
        self.play(FadeIn(cierre, shift=UP * 0.2))
        self.wait(1.5)

        final = Text(
            "La integral definida es el lÃ­mite de sumas con signo; coincide con el "
            "Ã¡rea solo si f no toma valores negativos.",
            font_size=21, color=GREY_A, line_spacing=1.15,
        ).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(final, shift=UP * 0.15))
        self.wait(3)


# =============================================================================
# ESCENA 10 - CREDITOS
# =============================================================================
class Creditos(Scene):
    """Fuentes, recursos externos y declaracion de IA."""

    def construct(self):
        self.play(Write(titulo("Fuentes y recursos")))

        fuentes = VGroup(
            Text("Apunte base: Introducción a la integral. MAT1188, 2026.",
                 font_size=21, color=GREY_A),
            Text("Stewart, J. CÃ¡lculo de una variable. 7Ãª ed. Cengage Learning.",
                 font_size=21, color=GREY_A),
            Text("Thomas, G. B. CÃ¡lculo. Una variable. 12Ãª ed. Pearson.",
                 font_size=21, color=GREY_A),
            Text("Documentación oficial de Manim Community (docs.manim.community).",
                 font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        fuentes.next_to(ORIGIN, UP, buff=0.6)

        ia = Text(
            "Declaración de IA: [completar: herramienta, finalidad, partes apoyadas "
            "y verificación].",
            font_size=19, color=GREY_B, line_spacing=1.1,
        ).to_edge(DOWN, buff=1.3)

        despedida = Text("Gracias.", font_size=34, color=GOLD).to_edge(DOWN, buff=0.5)

        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.15) for f in fuentes],
                              lag_ratio=0.25))
        self.wait(1.5)
        self.play(FadeIn(ia, shift=UP * 0.15))
        self.wait(1)
        self.play(Write(despedida))
        self.wait(3)

