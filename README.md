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
- `utils/comun.py` – Cálculos exactos, estilo, funciones de graficación y constructores reutilizables.
- `scenes/escenas.py` – Las 10 escenas que componen el video del proyecto (Manim Community 0.22.0).
- `README.md` – Este archivo.
- `render.py` y `render.ps1` – Renderizan y ensamblan las diez escenas en orden narrativo.
- Ficha de entrega: no está incluida en este repositorio; confirmar su formato con la pauta de entrega completa.
- `media/output/MAT1188_EID_G06_2026.mp4` – Video generado localmente; los renders no se versionan.

## Entorno y dependencias
Python 3.13 y Manim Community 0.22.0. Las dependencias de Python están fijadas en `requirements.txt`.
Manim necesita Cairo/Pango para texto y una distribución LaTeX con `latex` y `dvisvgm` para fórmulas.
FFmpeg debe estar en el PATH; el ensamblado también admite el ejecutable de `imageio-ffmpeg`.

En macOS, instalar las dependencias del sistema:
```sh
brew install pkgconf cairo pango texlive ffmpeg
```
En Windows, instalar MiKTeX y comprobar `latex --version` y `dvisvgm --version`.
Consultar la [instalación oficial de Manim](https://docs.manim.community/en/stable/installation.html) para otras plataformas.

Crear un entorno virtual desde la raíz del repositorio:
```sh
python -m venv .venv
```
Activarlo con `source .venv/bin/activate` en macOS/Linux o `.\.venv\Scripts\Activate.ps1` en PowerShell y ejecutar:
```sh
python -m pip install -r requirements.txt
```

## Ejecución
Los archivos actuales están en `scenes/escenas.py` y `utils/comun.py`. Ejecutar desde la raíz del repositorio.

**Una escena en calidad de prueba:**
```sh
python -m manim render -ql scenes/escenas.py Portada
```

**Las diez escenas y un único MP4 en orden narrativo:**
```sh
python render.py --quality ql
python render.py --quality qh
```
`ql` genera 480p15, `qm` 720p30, `qh` 1080p60 y `qk` 2160p60.
El resultado se guarda en `media/output/MAT1188_EID_G06_2026.mp4`.
Cada ejecución reemplaza ese resultado con la calidad elegida. Para conservar ambos, usar `--output media/output/preview.mp4` en la prueba.
El ensamblado incluye únicamente las diez escenas, desde Portada hasta Creditos, y falla si falta alguna o si FFmpeg falla.
Para unir renders existentes: `python render.py --quality qh --skip-render`.

En PowerShell se puede usar el mismo flujo con `.\render.ps1 -Calidad qh`.

**Verificación de cálculos y ensamblado:**
```sh
python -m unittest discover -s tests -v
```

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
8. **ComparacionFinal** – Barras de magnitudes para el área y flechas con signo para la integral, con origen y valor neto.
9. **RespuestaCentral** – Respuesta explícita a la pregunta central: $A^- > 0 \implies A^+-A^- < A^++A^-$.
10. **Creditos** – Fuentes, recursos externos y declaración de IA.

## Fuentes y recursos externos
- Apunte base: *Introducción a la integral*. MAT1188 – Cálculo Intermedio, 2026.
- Stewart, J. *Cálculo de una variable: Trascendentes tempranas*. 7ª ed. Cengage Learning.
- Thomas, G. B. et al. *Cálculo: Una variable*. 12ª ed. Pearson.
- Manim Community. Documentación oficial: [docs.manim.community](https://docs.manim.community/).

## Declaración de IA
Esta revisión utilizó Codex (OpenAI) para revisar el código, corregir la distribución visual y los scripts de render, y verificar cálculos y resultados renderizados.
Los créditos describen este apoyo. El equipo debe añadir en su entrega el detalle de cualquier uso previo de IA, que no se puede reconstruir a partir del repositorio.

## Notas técnicas
- Los cálculos ($A^+, A^-, \int, \text{área}$) están centralizados en `utils/comun.py` para asegurar coherencia entre escenas.
- Se emplea suma de Riemann de **punto medio** (transparente, evita ambigüedad y es fácil de visualizar).
- La partición se refina $n=6,12,24$ hasta aproximar a los valores exactos $-6$ y $46/3\approx 15,33$, mostrando el proceso de límite.
- Escalas y etiquetas visibles. Diferenciación clara entre rectángulos rojos/verde para enfatizar aportes con signo.
- El PDF de temas proporcionado define el tema del grupo 6, pero no fija una duración ni un formato de ficha. Confirmar esos requisitos con la pauta de entrega completa. El render es una animación sin narración; medir su duración real con FFprobe tras generarlo.