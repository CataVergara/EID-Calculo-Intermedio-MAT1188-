# Proyecto EID - Cálculo Intermedio (MAT1188) - Grupo 6

## Datos generales
- **Asignatura:** MAT1188 · Cálculo Intermedio
- **Curso:** Ingeniería Civil Informática · Segundo año
- **Modalidad:** Evaluación Integrada de Desempeño (EID)
- **Grupo:** 6
- **Tema asignado:** Eje 6 · Integral definida y área geométrica · *Contribuciones positivas y negativas*
- **Pregunta central:** *¿Por qué una integral definida puede ser menor que el área geométrica total?*

## Integrantes
- CATALINA JAVIERA VERGARA ALARCON – GitHub: [@CataVergara](https://github.com/CataVergara)
- IGNACIO ALEXANDER DE CELIS VALENCIA – GitHub: `IGNACIO ALEXANDER DE CELIS VALENCIA`
- MARCELO FABIÁN SANTANA ASTORGA – GitHub: `MARCELO FABIÁN SANTANA ASTORGA`

## Archivos principales
- `comun.py` – Cálculos exactos, estilo, funciones de graficación y constructores reutilizables.
- `escenas.py` – Las 10 escenas que componen el video del proyecto (Manim Community 0.22.0).
- `README.md` – Este archivo.
- `render.ps1` – Script para renderizar en alta calidad (1080p60) y unir escenas (facilita la obtención de un único MP4 si lo desea el equipo).
- `ficha.pdf` – Ficha de entrega (a generar: incluye curso, integrantes, tema, pregunta central, duración, enlace a repositorio, SHA del commit entregado, referencias y declaración de IA).
- `MAT1188_EID_G06_2026.mp4` – Video resultante una vez rendereado y unido (puede ajustarse al nombre solicitado por Blackboard).

## Entorno y dependencias
- Python 3.14.7
- Manim Community 0.22.0
- NumPy 2.5.3
- MiKTeX (pdflatex) 25.12 – necesario para fórmulas LaTeX.
- FFmpeg 7.1 (incluido vía `imageio-ffmpeg`) – para codificación de video.

Para instalar dependencias mínimas (si falta alguna):
```powershell
pip install manim==0.22.0 numpy imageio-ffmpeg
```

## Ejecución
Desde la carpeta del proyecto (`C:\Users\cata2\OneDrive\Desktop\EID Calculo Intermedio (MAT1188)\`):

**Renderizar una escena en calidad previa (rápido):**
```powershell
python -m manim render -ql escenas.py Portada
```

**Renderizar una escena en alta calidad (1080p15, recomendado para entrega):**
```powershell
python -m manim render -qh escenas.py Portada
```

**Renderizar todas las escenas en alta calidad:**
```powershell
python -m manim render -qh escenas.py
```

**Unir las escenas (OPCIONAL) para obtener un único MP4:**
```powershell
.\render.ps1
```
El script guarda el resultado en `media/videos/escenas/1080p15/VIDEO_FINAL.mp4` (o el nombre indicado). En el proyecto actual, el guion y la narración definieron las 10 escenas; unirlas en un solo archivo es útil para entregar `MATXXX_EID_G06_2026.mp4`. Verifique el límite (entre 4 y 6 minutos) tras la edición y ajuste de narración.

## Ejemplo principal
- **Función:** $f(x)=x^2-4$
- **Intervalo:** $[-3,3]$
- **Raíces:** $x=-2,\,2$
- **Regiones:** $[-3,-2]$ y $[2,3]$ con $f\ge 0$ (contribuciones positivas $A^+$); $[-2,2]$ con $f<0$ (contribución negativa $A^-$, en valor absoluto).
- **Valores exactos (verificados):**
  - $A^+ = \int_{-3}^{-2}(x^2-4)dx + \int_{2}^{3}(x^2-4)dx = \frac{7}{3}+\frac{7}{3}=\frac{14}{3}\approx 4,6667$
  - $A^- = \int_{-2}^{2}(-(x^2-4))dx = \frac{32}{3}\approx 10,6667$
  - $\int_{-3}^{3}(x^2-4)dx = A^+ - A^- = -6$
  - Área geométrica total = $A^+ + A^- = \frac{46}{3}\approx 15,3333$

## Escenas del video
1. **Portada** – Presentación, integrantes, tema y pregunta central.
2. **TeoriaSigno** – ¿Por qué aparecen aportes positivos y negativos al sumar $f(x_i^*)\Delta x$?
3. **TeoriaDefiniciones** – Diferencia entre integral definida ($A^+ - A^-$) y área geométrica ($A^++A^-$).
4. **EjemploPrincipal** – $f(x)=x^2-4$ en $[-3,3]$: raíces, signo y regiones.
5. **Rectangulos** – Suma de Riemann de punto medio con $n=6$: partición, $\Delta x$, puntos muestra y rectángulos.
6. **SumaDeAportes** – Sumamos aportes: obtenemos $S_6 = -6,5$ (aprox. integral) vs área $15,5$.
7. **Refinamiento** – $n=6 \to 12 \to 24$: $S_n \to -6$ y área $\to 46/3$. Muestra el límite de la suma de Riemann.
8. **ComparacionFinal** – Comparación visual de barras (verde/rojo) entre integral y área geométrica.
9. **RespuestaCentral** – Respuesta explícita a la pregunta central: $A^- > 0 \implies A^+-A^- < A^++A^-$.
10. **Creditos** – Fuentes, recursos externos y declaración de IA.

## Fuentes y recursos externos
- Apunte base: *Introducción a la integral*. MAT1188 – Cálculo Intermedio, 2026.
- Stewart, J. *Cálculo de una variable: Trascendentes tempranas*. 7ª ed. Cengage Learning.
- Thomas, G. B. et al. *Cálculo: Una variable*. 12ª ed. Pearson.
- Manim Community. Documentación oficial: [docs.manim.community](https://docs.manim.community/).

## Declaración de IA
Declarar en `ficha.pdf`:
- **Herramienta:** (ej.: ChatGPT, Claude, Gemini, Copilot u otra) – especificar versión.
- **Finalidad:** (ej.: apoyo en escritura, creación de guion, revisión matemática, generación de README, estructura de código Manim).
- **Partes apoyadas:** indicar archivos, secciones o funciones.
- **Verificación:** cómo se verificaron los cálculos, fórmulas y resultados (comparación con valores exactos, revisión manual, ensayo de render).
- **Nota:** En caso de no usar IA, declarar explícitamente: *"No se utilizó inteligencia artificial en la realización de este proyecto."*

## Notas técnicas
- Los cálculos ($A^+, A^-, \int, \text{área}$) están centralizados en `comun.py` para asegurar coherencia entre escenas (apoyo al criterio V2/V3 y a la defensa D2/D4).
- Se emplea suma de Riemann de **punto medio** (transparente, evita ambigüedad y es fácil de visualizar).
- La partición se refina $n=6,12,24$ hasta aproximar a los valores exactos $-6$ y $46/3\approx 15,33$, mostrando el proceso de límite (criterio V1/V3 y defensa D1).
- Escalas y etiquetas visibles (criterio V4). Diferenciación clara entre rectángulos rojos/verde para enfatizar aportes con signo (criterio V5).
- Duración aproximada total de las escenas renderizadas: **2 min 56 s**. Tras añadir narración, transiciones, silencios y edición, el video MP4 deberá ajustarse al rango **4–6 minutos** exigido (sección 2 de la pauta).