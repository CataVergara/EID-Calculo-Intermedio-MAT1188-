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
- `scenes/escenas.py`: las diez escenas del video, con fórmulas, rótulos y pausas para el guion.
- `utils/guion.py`: orden, duración de cada escena e identificación de las voces. El montaje actual dura 5:21.
- `utils/edicion.py`: tomas elegidas y recorte de una repetición en la voz de Ignacio.
- `montar.py`: extrae y nivela las voces, las une con el video y prepara archivos separados para CapCut.
- `README.md` – Este archivo.
- `render.py` y `render.ps1` – Renderizan y ensamblan las diez escenas en orden narrativo.
- [Guion del video](docs/guion.pdf) y [ficha de entrega](docs/MAT1188_EID_G06_2026.pdf): documentos incorporados por el equipo. Completar la ficha con los datos del video definitivo.
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

**Montaje con las dos grabaciones disponibles:**
```sh
python montar.py --catalina "/ruta/catalina.mov" --ignacio "/ruta/ignacio.mp4" --salida media/output/montaje
```
Ejecutar primero el render en `qh`. El montaje comprueba que las diez escenas tengan los tiempos actuales y estén en 1080p60, para evitar mezclar grabaciones con renders antiguos.

Los archivos recibidos se usan únicamente como fuentes de audio. Sus imágenes no aparecen en el montaje. La salida incluye un borrador con las voces, el video sin sonido, una pista de voces alineada desde cero y las escenas y audios separados para CapCut. `Tiempos_CapCut.csv` indica sus posiciones. Las grabaciones y los renders permanecen fuera de Git.

El bloque de Marcelo empieza en 3:36 y conserva los 105 segundos propuestos hasta recibir su grabación. El borrador contiene silencio en esa parte. Hay que incorporar la tercera voz y revisar su sincronización antes de entregar.

Los recortes se fijan en `utils/edicion.py`. En la grabación recibida de Ignacio se omite de 152,45 a 153,60 segundos para reducir una repetición del setenta y cinco, conservando el final del número. No se modifica la velocidad ni se genera voz. Los bordes se suavizan y el volumen se nivela por persona. Para comprobar solo los audios se puede añadir `--solo-audio` al comando anterior.

**Apoyos visuales:** los recuadros señalan el símbolo y el objeto que se están explicando. Permanecen visibles durante la explicación y se sustituyen al cambiar el foco. Se retiran junto con su contenido o al terminar la escena. El ancho, el punto muestra y la altura se conectan con un mismo rectángulo. Después se desarrolla el ejemplo de $x^*=2,5$, con altura y aporte $2,25$. Los cuatro aportes negativos se señalan uno a uno, junto con los signos de resta y suma y el valor absoluto. Los colores de $A^+$ y $A^-$ se mantienen en las fórmulas.

**Verificación de cálculos y ensamblado:**
```sh
python -m unittest discover -s tests -v
```

## Ejemplo principal
- **Función:** $f(x)=x^2-4$
- **Intervalo:** $[-3,3]$
- **Raíces:** $x=-2,\,2$
- **Regiones:** $[-3,-2]$ y $[2,3]$ con $f\ge 0$ (contribuciones positivas $A^+$); $(-2,2)$ con $f<0$ (contribución negativa $A^-$, en valor absoluto).
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
8. **ComparacionFinal**: cálculo exacto de las tres regiones con una antiderivada, seguido de barras para el área y flechas para la integral.
9. **RespuestaCentral** – Respuesta explícita a la pregunta central: $A^- > 0 \implies A^+-A^- < A^++A^-$.
10. **Creditos** – Fuentes, recursos externos y declaración de IA.

## Fuentes y recursos externos
- Apunte base: *Introducción a la integral*. MAT1188 – Cálculo Intermedio, 2026.
- Stewart, J. *Cálculo de una variable: Trascendentes tempranas*. 7ª ed. Cengage Learning.
- Thomas, G. B. et al. *Cálculo: Una variable*. 12ª ed. Pearson.
- Manim Community. Documentación oficial: [docs.manim.community](https://docs.manim.community/).

## Declaración de IA
El equipo declara el apoyo de Claude (Anthropic) en la guía de trabajo y el borrador inicial del código, y de Codex (OpenAI) en la revisión del código, las escenas, el guion, la ficha, las pruebas y el montaje con FFmpeg. La ficha contiene el detalle de usos y verificación y debe actualizarse con el montaje final. Las grabaciones deben realizarse con las voces de los tres integrantes.

## Notas técnicas
- Los cálculos ($A^+, A^-, \int, \text{área}$) están centralizados en `utils/comun.py` para asegurar coherencia entre escenas.
- Se emplea suma de Riemann de **punto medio** (transparente, evita ambigüedad y es fácil de visualizar).
- La partición se refina $n=6,12,24$ hasta aproximar a los valores exactos $-6$ y $46/3\approx 15,33$, mostrando el proceso de límite.
- Escalas y etiquetas visibles. Diferenciación clara entre rectángulos rojos/verde para enfatizar aportes con signo.
- La rúbrica exige un video de 4 a 6 minutos con las tres voces. `docs/guion.pdf` conserva la propuesta inicial de 5:15. Los tiempos de Catalina e Ignacio se ajustaron a sus grabaciones y el montaje actual dura 5:21. Falta la voz de Marcelo.
- Las pausas se distribuyen entre los pasos de cada explicación con `esperar_hasta()`. `finalizar()` completa el tiempo reservado y avisa si una escena lo sobrepasa. Los tiempos se cuentan desde el inicio de cada escena.
- Antes de modificar los tiempos, ensayar las voces y actualizar `utils/guion.py` y los puntos de pausa afectados. La duración propuesta no sustituye la revisión del montaje con audio.
- El render utiliza `utils/comun.py` y `scenes/escenas.py`.
- Ver el [informe de revisión del issue #5](docs/REVISION_ISSUE_5.md) para conocer el estado del aporte y la validación de las correcciones.

## Tiempos actuales del montaje

| Escena | Inicio | Fin | Duración | Voz |
|---|---|---|---:|---|
| Portada | 0:00 | 0:10,65 | 10,65 s | Catalina |
| TeoriaSigno | 0:10,65 | 0:46,95 | 36,30 s | Catalina |
| TeoriaDefiniciones | 0:46,95 | 1:27,60 | 40,65 s | Catalina |
| EjemploPrincipal | 1:27,60 | 2:01,20 | 33,60 s | Ignacio |
| Rectangulos | 2:01,20 | 2:37,95 | 36,75 s | Ignacio |
| SumaDeAportes | 2:37,95 | 3:36 | 58,05 s | Ignacio |
| Refinamiento | 3:36 | 4:01 | 25 s | Marcelo |
| ComparacionFinal | 4:01 | 4:51 | 50 s | Marcelo |
| RespuestaCentral | 4:51 | 5:11 | 20 s | Marcelo |
| Creditos | 5:11 | 5:21 | 10 s | Marcelo |
