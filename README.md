# Proyecto EID - Cálculo Intermedio (MAT1188) - Grupo 6

## Datos generales
- **Asignatura:** MAT1188 · Cálculo Intermedio
- **Curso:** Ingeniería Civil Informática · Segundo año
- **Modalidad:** Evaluación Integrada de Desempeño (EID)
- **Grupo:** 6
- **Tema asignado:** Eje 6 · Integral definida y área geométrica · *Contribuciones positivas y negativas*
- **Pregunta central:** *¿Por qué una integral definida puede ser menor que el área geométrica total?*

## Integrantes
- CATALINA JAVIERA VERGARA ALARCON - GitHub: [@CataVergara](https://github.com/CataVergara)
- IGNACIO ALEXANDER DE CELIS VALENCIA - GitHub: [@idecelis2017-hub](https://github.com/idecelis2017-hub)
- MARCELO FABIÁN SANTANA ASTORGA - GitHub: [@cchelooo](https://github.com/cchelooo)

## Archivos principales
- `utils/comun.py` - Cálculos exactos, estilo, funciones de graficación y constructores reutilizables.
- `scenes/escenas.py`: las diez escenas del video, con fórmulas, rótulos y pausas para el guion.
- `utils/guion.py`: orden, duración de cada escena e identificación de las voces. El montaje actual dura 5:15.
- `utils/edicion.py`: tomas elegidas, recortes de repeticiones y ajustes de las pausas de voz.
- `montar.py`: extrae y nivela las voces, las une con el video y prepara archivos separados para CapCut.
- `README.md` - Este archivo.
- `render.py` y `render.ps1` - Renderizan y ensamblan las diez escenas en orden narrativo.
- [Guion del video](docs/guion.pdf) y [ficha de entrega](docs/MAT1188_EID_G06_2026.pdf): documentos del montaje final. Las fuentes editables están en la misma carpeta. El curso corresponde a MAT1188, sección 1.
- `media/output/MAT1188_EID_G06_2026.mp4` - Video generado localmente; los renders no se versionan.

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

**Montaje con las tres voces:**
```sh
python montar.py \
  --catalina "/ruta/catalina.mov" \
  --ignacio "/ruta/ignacio.mp4" \
  --marcelo-refinamiento "/ruta/marcelo_refinamiento.mp4" \
  --marcelo-comparacion "/ruta/marcelo_comparacion.mp4" \
  --marcelo-respuesta "/ruta/marcelo_respuesta.mp4" \
  --marcelo-creditos "/ruta/marcelo_creditos.mp4" \
  --salida media/output/montaje
```
Ejecutar primero el render en `qh`. El montaje comprueba que las diez escenas tengan los tiempos actuales y estén en 1080p60, para evitar mezclar grabaciones con renders antiguos.

Los archivos recibidos se usan como fuentes de audio. La salida incluye `MAT1188_EID_G06_2026.mp4`, el video sin sonido, una pista de voces alineada desde cero y las escenas y audios separados para CapCut. `Tiempos_CapCut.csv` indica sus posiciones y si cada grabación está disponible. Si se omite algún archivo de Marcelo, la salida se identifica como borrador y señala las escenas pendientes. Las grabaciones y los renders permanecen fuera de Git.

Los recortes e insertos se fijan en `utils/edicion.py` y corresponden a las grabaciones originales utilizadas. En Catalina se añade una pausa de 0,25 segundos después de «A más». También se separan las frases sobre el signo del área, la resta de A menos a A más y el área total. Se acortan silencios al inicio y al final de la escena para conservar los tiempos del montaje. En Ignacio se reduce una repetición del setenta y cinco. En Marcelo se seleccionan las tomas completas y se conserva la frase correcta «aproximadamente quince coma treinta y tres», con el valor exacto 46/3 visible. No se modifica la velocidad ni se genera voz. Los bordes se suavizan y el volumen se nivela por persona. Para comprobar solo los audios se puede añadir `--solo-audio` al comando anterior.

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
1. **Portada** - Presentación, integrantes, tema y pregunta central.
2. **TeoriaSigno** - ¿Por qué aparecen aportes positivos y negativos al sumar $f(x_i^*)\Delta x$?
3. **TeoriaDefiniciones** - Diferencia entre integral definida ($A^+ - A^-$) y área geométrica ($A^++A^-$).
4. **EjemploPrincipal** - $f(x)=x^2-4$ en $[-3,3]$: raíces, signo y regiones.
5. **Rectangulos** - Suma de Riemann de punto medio con $n=6$: partición, $\Delta x$, puntos muestra y rectángulos.
6. **SumaDeAportes** - Sumamos aportes: obtenemos $S_6 = -6,5$ (aprox. integral) vs área $15,5$.
7. **Refinamiento** - $n=6 \to 12 \to 24$: $S_n \to -6$ y área $\to 46/3$. Muestra el límite de la suma de Riemann.
8. **ComparacionFinal**: cálculo exacto de las tres regiones con una antiderivada, seguido de barras para el área y flechas para la integral.
9. **RespuestaCentral** - Respuesta explícita a la pregunta central: $A^- > 0 \implies A^+-A^- < A^++A^-$.
10. **Creditos** - Fuentes, recursos externos y declaración de IA.

## Fuentes y recursos externos
El [registro de referencias y apoyo de IA](docs/REFERENCIAS.md) contiene el apunte, las ediciones y enlaces verificados de Stewart y Thomas, los recursos de Manim y FFmpeg, y el uso de Claude y Codex. Incluye las páginas que el equipo debe repasar antes de la defensa. Las voces provienen de las grabaciones de los tres integrantes.

La [revisión de la entrega](docs/REVISION_ENTREGA.md) compara los cuatro documentos del curso y deja indicados los datos que requieren confirmación. La declaración de IA no necesita leerse en voz alta. Los créditos se muestran en pantalla y el registro completo queda enlazado aquí y en la ficha.

## Notas técnicas
- Los cálculos ($A^+, A^-, \int, \text{área}$) están centralizados en `utils/comun.py` para asegurar coherencia entre escenas.
- Se emplea suma de Riemann de **punto medio** (transparente, evita ambigüedad y es fácil de visualizar).
- La partición se refina $n=6,12,24$ hasta aproximar a los valores exactos $-6$ y $46/3\approx 15,33$, mostrando el proceso de límite.
- Escalas y etiquetas visibles. Diferenciación clara entre rectángulos rojos/verde para enfatizar aportes con signo.
- La rúbrica exige un video de 4 a 6 minutos con las tres voces. El montaje completo dura 5:15, con los tiempos del guion ajustados a las grabaciones.
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
| ComparacionFinal | 4:01 | 4:45 | 44 s | Marcelo |
| RespuestaCentral | 4:45 | 5:03 | 18 s | Marcelo |
| Creditos | 5:03 | 5:15 | 12 s | Marcelo |
