# Revisión del aporte para el issue #5

Revisión local del 16 de octubre de 2026 en la rama `santana`, después de actualizarla con `origin/main` mediante avance directo hasta `35c4817`.

## Estado del aporte recibido

El aporte de `De Celis/comun.py` no completa el issue #5. Al iniciar la revisión, su contenido era idéntico, byte por byte, al de `utils/comun.py` en el commit `35c4817`.

Además, `scenes/escenas.py` importa `utils.comun` y `render.py` ejecuta las escenas de `scenes/escenas.py`. Ninguno utiliza el archivo de la carpeta `De Celis`. Por eso el aporte recibido no modifica las fórmulas, los rótulos ni la duración del video que genera el proyecto.

Se conserva esa copia como referencia. Las correcciones de esta revisión se realizan en los archivos que utiliza el render.

## Correcciones realizadas

| Parte del issue | Cambio local |
|---|---|
| Área e integral del valor absoluto | La escena TeoriaDefiniciones muestra la integral de valor absoluto y la suma A⁺+A⁻. |
| Antiderivada y pasos exactos | ComparacionFinal presenta F(x)=x³/3−4x, su derivada y la evaluación de cada intervalo. |
| Tres regiones | Se muestran 7/3 y 7/3 para las regiones exteriores, A⁺=14/3 y la integral central −32/3, cuya área es A⁻=32/3. |
| Comparación de resultados | Después del cálculo se animan las barras del área y las flechas de la integral hasta −6. |
| Identificación de las voces | Cada escena incluye el nombre de quien explica, según el reparto del guion. |
| Tiempos | El orden y las duraciones se centralizan en `utils/guion.py`, con tres bloques de 105 segundos y un total de 315 segundos. |
| Pausas | Se distribuyen entre los pasos de la explicación con `esperar_hasta()`. Se genera un error si una animación sobrepasa un punto previsto del guion. |
| Créditos | Se incluyen las referencias, Claude, Codex y la comprobación de los resultados, de acuerdo con la ficha proporcionada por el equipo. |

## Validación

- Las 11 pruebas aprobaron, incluidas la ejecución de las diez escenas, su duración prevista y la revisión automática de textos.
- Se revisaron imágenes finales de las diez escenas y los estados intermedios de las definiciones y el cálculo exacto.
- El MP4 de prueba se generó en 480p15. Cada escena contiene exactamente los cuadros previstos. El total es de 4725 cuadros, equivalentes a 315 segundos a 15 cuadros por segundo.
- Se generó y revisó también la versión 1080p60. Cada escena contiene los cuadros previstos y el MP4 completo tiene 18900 cuadros, equivalentes a 315 segundos a 60 cuadros por segundo. FFprobe confirma una duración de 5:15.
- La duración coincide con la tabla de `docs/guion.pdf`: 5:15 en total.
- Los dos renders terminaron sin avisos de textos superpuestos. La comprobación incluye la revisión visual de los pasos nuevos del cálculo.

## Lo que sigue pendiente para la entrega

El video base no contiene las grabaciones de voz. Las pausas siguen el guion escrito, pero el ajuste definitivo a la narración solo puede comprobarse cuando estén las tres grabaciones. Después hay que revisar el montaje con audio y completar duración, enlace y versión final en la ficha de entrega.

Esta revisión no acredita por sí sola el cierre del issue: el equipo debe revisar el resultado, incorporar las voces y aportar la evidencia acordada en GitHub. Las modificaciones de código están en la rama `santana`.
