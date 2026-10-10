## Guía: Permitir Python/Manim (Control de Aplicaciones)

El error "DLL load failed while importing opaque" suele deberse a Control de Aplicaciones (WDAC/Smart App Control).

### Opción 1: Permitir carpeta de Python
1. Abrir Seguridad de Windows > Protección contra virus y amenazas > Configuración de Protección contra virus y amenazas (Administrar configuración)
2. Ir a "Control de aplicaciones y navegador" > "Control de aplicaciones" > Configuración de Control de aplicaciones
3. Si está en "Bloquear" o "Modo estricto", cambiar a "Avisar" (más permisivo) o agregar excepción.

### Opción 2: Excluir rutas
Añadir exclusiones:
- C:\Python314\
- C:\Users\cata2\AppData\Roaming\Python\
- C:\Users\cata2\AppData\Local\Programs\Python\ (si existe)

Seguridad de Windows > Protección contra virus y amenazas > Administrar configuración > Exclusiones > Añadir exclusión > Carpeta.

### Opción 3: Smart App Control
Si tienes Smart App Control (Windows 11): Configuración > Privacidad y seguridad > Seguridad de Windows > Aplicaciones y navegador > Smart App Control -> desactivar temporalmente.

### Comprobar
Después, abrir terminal en la carpeta y probar:
`powershell
cd "C:\Users\cata2\OneDrive\Desktop\EID-Calculo-Intermedio-MAT1188-G06"
py -m manim --version
# o
python -m manim --version
`

Nota: Si eres administrador puede tardar un poco en aplicar.
