# EID de Cálculo Intermedio, Grupo 6

Proyecto de MAT1188, sección 1, Ingeniería Civil Informática, 2026.

**Tema:** integral definida y área geométrica, con contribuciones positivas y negativas.

**Pregunta central:** ¿por qué una integral definida puede ser menor que el área geométrica total?

## Integrantes

- Catalina Javiera Vergara Alarcón: [@CataVergara](https://github.com/CataVergara).
- Ignacio Alexander De Celis Valencia: [@idecelis2017-hub](https://github.com/idecelis2017-hub).
- Marcelo Fabián Santana Astorga: [@cchelooo](https://github.com/cchelooo).

## Archivos principales

- `scenes/escenas.py`: las diez escenas de Manim.
- `utils/comun.py`: cálculos, colores y elementos gráficos compartidos.
- `utils/guion.py`: orden, duración de las escenas e identificación de las voces.
- `render.py` y `render.ps1`: generación y unión de las escenas.
- `requirements.txt`: dependencias de Python.
- `tests/`: comprobaciones de los cálculos, las escenas y el ensamblado.
- `docs/`: ficha de entrega, referencias y material del curso.

## Instalación

Se utilizó Python 3.13 y Manim Community 0.22.0. Se necesitan FFmpeg, Cairo, Pango y una distribución LaTeX con `latex` y `dvisvgm`. Consultar la [instalación oficial de Manim](https://docs.manim.community/en/stable/installation.html) para los requisitos del sistema.

Desde la raíz del repositorio:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows, activar el entorno con `.\.venv\Scripts\Activate.ps1` en PowerShell.

## Generar las animaciones

```sh
python render.py --quality qh
```

Genera las diez escenas en 1080p60 y las une, sin narración, en `media/output/MAT1188_EID_G06_2026.mp4`. Para una prueba rápida se puede usar `--quality ql`. En PowerShell también está disponible `.\render.ps1 -Calidad qh`.

El video entregado incorpora las voces de los tres integrantes y dura 5 minutos y 15 segundos. Para los recortes iniciales de audio se utilizó un programa auxiliar, `montar.py`, basado en FFmpeg. Después se ajustaron las pausas, las uniones y la sincronización con las animaciones. Las grabaciones se conservan fuera de este repositorio.

## Ejemplo y escenas

Se estudia $f(x)=x^2-4$ en $[-3,3]$, con raíces en $-2$ y $2$. Las regiones positivas tienen área total $14/3$ y la región negativa tiene área $32/3$.

$$
\int_{-3}^{3}f(x)\,dx=-6,\qquad
\int_{-3}^{3}|f(x)|\,dx=\frac{46}{3}\approx15{,}33.
$$

| Escena | Contenido |
|---|---|
| Portada | Integrantes, tema y pregunta central. |
| TeoriaSigno | Contribuciones positivas y negativas. |
| TeoriaDefiniciones | Diferencia entre integral y área geométrica. |
| EjemploPrincipal | Función, intervalo, raíces y regiones. |
| Rectangulos | Suma de Riemann de punto medio con seis rectángulos. |
| SumaDeAportes | Cálculo de las aproximaciones de integral y área. |
| Refinamiento | Aumento del número de rectángulos y acercamiento a los valores exactos. |
| ComparacionFinal | Cálculo exacto y comparación de resultados. |
| RespuestaCentral | Respuesta a la pregunta del proyecto. |
| Creditos | Fuentes, recursos y declaración de IA. |

## Comprobaciones

```sh
python -m unittest discover -s tests -v
```

## Documentación

- [Ficha de entrega](docs/MAT1188_EID_G06_2026.pdf), con el SHA del código utilizado, y su [fuente LaTeX](docs/ficha.tex).
- [Referencias y declaración de IA](docs/REFERENCIAS.md).
- [Material del curso](docs/curso/README.md): temas por grupo, pauta, rúbrica y apunte base.
