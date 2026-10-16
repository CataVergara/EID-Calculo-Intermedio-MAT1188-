"""Orden, duración y voz de las escenas, según docs/guion.pdf."""

# Los segundos corresponden al video sin las grabaciones. Después de ensayar,
# cualquier ajuste del guion se hace aquí y en los puntos de cada escena.
GUION = {
    "Portada": (15, "Catalina Vergara"),
    "TeoriaSigno": (45, "Catalina Vergara"),
    "TeoriaDefiniciones": (45, "Catalina Vergara"),
    "EjemploPrincipal": (30, "Ignacio De Celis"),
    "Rectangulos": (35, "Ignacio De Celis"),
    "SumaDeAportes": (40, "Ignacio De Celis"),
    "Refinamiento": (25, "Marcelo Santana"),
    "ComparacionFinal": (50, "Marcelo Santana"),
    "RespuestaCentral": (20, "Marcelo Santana"),
    "Creditos": (10, "Marcelo Santana"),
}

DURACION_TOTAL = sum(duracion for duracion, _ in GUION.values())
