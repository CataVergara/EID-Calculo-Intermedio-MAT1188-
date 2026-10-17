"""Orden y tiempos del montaje con las grabaciones disponibles."""

# Catalina e Ignacio siguen sus grabaciones. El bloque de Marcelo conserva
# los 105 segundos propuestos en el guion hasta recibir su voz.
GUION = {
    "Portada": (10.65, "Catalina Vergara"),
    "TeoriaSigno": (36.30, "Catalina Vergara"),
    "TeoriaDefiniciones": (40.65, "Catalina Vergara"),
    "EjemploPrincipal": (33.60, "Ignacio De Celis"),
    "Rectangulos": (36.75, "Ignacio De Celis"),
    "SumaDeAportes": (58.05, "Ignacio De Celis"),
    "Refinamiento": (25, "Marcelo Santana"),
    "ComparacionFinal": (50, "Marcelo Santana"),
    "RespuestaCentral": (20, "Marcelo Santana"),
    "Creditos": (10, "Marcelo Santana"),
}

DURACION_TOTAL = sum(duracion for duracion, _ in GUION.values())
