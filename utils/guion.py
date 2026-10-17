"""Orden y tiempos del montaje con las grabaciones disponibles."""

# Los tiempos siguen las tomas elegidas de las tres voces.
GUION = {
    "Portada": (10.65, "Catalina Vergara"),
    "TeoriaSigno": (36.30, "Catalina Vergara"),
    "TeoriaDefiniciones": (40.65, "Catalina Vergara"),
    "EjemploPrincipal": (33.60, "Ignacio De Celis"),
    "Rectangulos": (36.75, "Ignacio De Celis"),
    "SumaDeAportes": (58.05, "Ignacio De Celis"),
    "Refinamiento": (25, "Marcelo Santana"),
    "ComparacionFinal": (44, "Marcelo Santana"),
    "RespuestaCentral": (18, "Marcelo Santana"),
    "Creditos": (12, "Marcelo Santana"),
}

DURACION_TOTAL = sum(duracion for duracion, _ in GUION.values())
