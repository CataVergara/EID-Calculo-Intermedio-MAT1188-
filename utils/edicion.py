"""Tomas elegidas, en segundos del archivo original de cada voz.

No se publican grabaciones. Los archivos se proporcionan a montar.py.
En SumaDeAportes se retira una repetición entre dos pausas, sin cambiar
la velocidad ni el orden de los cuatro aportes negativos.
"""

from math import isfinite

from utils.guion import GUION

RECORTES = {
    "Portada": ((7.55, 18.20),),
    "TeoriaSigno": ((18.20, 54.50),),
    "TeoriaDefiniciones": ((54.50, 94.65),),
    "EjemploPrincipal": ((0.20, 33.80),),
    "Rectangulos": ((87.35, 124.10),),
    "SumaDeAportes": ((128.40, 152.45), (153.60, 187.10)),
    "Refinamiento": ((0.10, 24.75),),
    "ComparacionFinal": ((0.25, 19.65), (20.05, 23.95), (32.55, 35.00),
                         (47.75, 54.30), (57.55, 63.98), (65.70, 68.50)),
    "RespuestaCentral": ((0.40, 8.60), (11.10, 15.80), (18.05, 22.25)),
    "Creditos": ((2.05, 11.85),),
}


def duracion_audio(tramos):
    return sum(fin - inicio for inicio, fin in tramos)


def validar_recortes(recortes=RECORTES, guion=GUION):
    """Impide cortar palabras por un audio mayor al espacio reservado."""
    for escena, tramos in recortes.items():
        if escena not in guion or not tramos:
            raise ValueError(f"Escena o recortes no válidos: {escena}")
        anterior = 0
        for inicio, fin in tramos:
            if not all(isfinite(x) for x in (inicio, fin)) or not 0 <= inicio < fin:
                raise ValueError(f"Recorte no válido en {escena}: {inicio}, {fin}")
            if inicio < anterior:
                raise ValueError(f"Recortes desordenados o superpuestos: {escena}")
            anterior = fin
        if duracion_audio(tramos) > guion[escena][0] + 1 / 48000:
            raise ValueError(f"La voz excede el tiempo de {escena}. Ajustar el guion.")
