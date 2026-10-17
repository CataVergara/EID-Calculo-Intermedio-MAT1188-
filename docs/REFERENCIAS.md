# Referencias y apoyo de IA

## Material matemático

1. Equipo docente de Cálculo Intermedio (MAT1188). (2026). *Introducción a la integral*. Apunte distribuido en Blackboard. El archivo no identifica autores individuales.
2. Stewart, J. (2012). *Cálculo de una variable. Trascendentes tempranas*. 7.ª edición. Cengage Learning. ISBN de la copia digital: 978-607-481-881-9. [PDF alojado por la Universidad de la República](https://eva.interior.udelar.edu.uy/pluginfile.php/96366/mod_resource/content/1/Stewart.%20C%C3%A1lculo%20de%20una%20variable..pdf). La sección 5.2 explica el área neta en la página impresa 373 y la regla del punto medio en la 378. Corresponden a las páginas 406 y 411 del PDF.
3. Thomas, G. B., Weir, M. D. y Hass, J. (2010). *Cálculo. Una variable*. 12.ª edición. Pearson Educación. ISBN: 978-607-32-0164-3. [PDF alojado por la Universidad Nacional de Cuyo](https://fcen.uncuyo.edu.ar/upload/calculo-de-una-variable-thomas-12ed.pdf). La sección 5.4, páginas impresas 280 y 281, distingue la integral del área total y explica la suma de valores absolutos por tramos. Corresponden a las páginas 300 y 301 del PDF.

Las ediciones, los años y las páginas anteriores se comprobaron en los PDF enlazados. No se presupone que cada integrante haya leído los libros completos. El equipo debe repasar estos apartados antes de la defensa y explicar las ideas con sus propias palabras.

El ejemplo del proyecto usa x² − 4 en el intervalo de −3 a 3, distinto del apunte base. La comprobación del tramo central coincide con el ejemplo 6 de Thomas, que estudia esa función entre −2 y 2. Nuestro desarrollo incluye además las dos regiones exteriores y las aproximaciones con 6, 12 y 24 rectángulos. Esta coincidencia se identifica como referencia de apoyo, sin atribuir al libro el código ni el montaje del proyecto.

## Herramientas y recursos

- Manim Community 0.22.0. [Documentación oficial](https://docs.manim.community/). Construcción de gráficas, fórmulas, rectángulos y animaciones.
- FFmpeg. [Sitio oficial](https://ffmpeg.org/). Extracción y recorte de las voces, nivelación de volumen, unión y exportación del MP4.
- Whisper, de OpenAI, utilizado mediante [faster-whisper](https://github.com/SYSTRAN/faster-whisper). Transcripción local para localizar frases, repeticiones y posibles errores. Las transcripciones no se presentan como subtítulos ni sustituyen la comprobación de los números y los cortes.

## Declaración de IA

| Herramienta | Finalidad y partes apoyadas | Comprobación |
|---|---|---|
| Claude, de Anthropic | Guía inicial, propuesta del ejemplo, borrador del código y apoyo en texto y distribución visual, según la declaración original del equipo | Comparación con el apunte, las referencias, los cálculos exactos y la ejecución del código |
| Codex, de OpenAI | Revisión del código, cálculos, resaltados, guion, ficha, fuentes, pruebas y montaje con las grabaciones recibidas | Pruebas del repositorio, evaluación con una antiderivada, revisión de fotogramas, duración y reproducción técnica del MP4 |
| Whisper, de OpenAI | Transcripción para seleccionar tomas y localizar repeticiones en las voces | Comparación con el guion, las pausas y los valores matemáticos. Se conservan los originales para revisar cualquier recorte |

Las narraciones provienen de las grabaciones de Catalina, Ignacio y Marcelo. No se generaron ni clonaron voces. La edición conserva su velocidad natural. El equipo debe revisar el video completo y comprender tanto la matemática como el código antes de entregar.
