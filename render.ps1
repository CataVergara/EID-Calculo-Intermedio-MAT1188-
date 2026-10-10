# Renderiza las 10 escenas EN ORDEN y las une en un solo video.
# Uso (desde la carpeta que contiene scenes/ y utils/):
#   powershell -ExecutionPolicy Bypass -File .\render.ps1            (calidad final 1080p60)
#   powershell -ExecutionPolicy Bypass -File .\render.ps1 -Calidad ql (prueba rapida 480p15)
param(
  [string]$Calidad = "qh",          # ql=480p15, qm=720p30, qh=1080p60
  [string]$Salida  = "VIDEO_FINAL.mp4"
)

Set-Location $PSScriptRoot
$carpetas = @{ ql = "480p15"; qm = "720p30"; qh = "1080p60"; qk = "2160p60" }
if (-not $carpetas.ContainsKey($Calidad)) { Write-Host "Calidad invalida. Use ql, qm, qh o qk."; exit 1 }

# ORDEN DEL VIDEO (no alfabetico)
$escenas = @("Portada", "TeoriaSigno", "TeoriaDefiniciones", "EjemploPrincipal",
             "Rectangulos", "SumaDeAportes", "Refinamiento", "ComparacionFinal",
             "RespuestaCentral", "Creditos")

foreach ($e in $escenas) {
  Write-Host "=== Renderizando $e ==="
  python -m manim "-$Calidad" scenes/escenas.py $e
  if ($LASTEXITCODE -ne 0) { Write-Host "Fallo en la escena $e. Revise el error de arriba."; exit 1 }
}

$Base = Join-Path $PSScriptRoot ("media\videos\escenas\" + $carpetas[$Calidad])

# Buscar ffmpeg (en el PATH o dentro de imageio_ffmpeg)
$ffmpeg = $null
$cmd = Get-Command ffmpeg -ErrorAction SilentlyContinue
if ($cmd) { $ffmpeg = $cmd.Source }
if (-not $ffmpeg) {
  $ffmpeg = python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())" 2>$null
}
if (-not $ffmpeg) {
  Write-Host ""
  Write-Host "No se encontro ffmpeg, asi que los videos NO se unieron."
  Write-Host "Las escenas estan en: $Base"
  Write-Host "Importelas en su editor (DaVinci, CapCut, Clipchamp) en este orden:"
  $escenas | ForEach-Object { Write-Host "  $_.mp4" }
  exit 0
}

# Lista de union con nombres relativos (evita problemas con tildes y espacios en la ruta)
$lista = Join-Path $Base "concat_list.txt"
$escenas | ForEach-Object { "file '$_.mp4'" } | Set-Content -Path $lista -Encoding ascii
Push-Location $Base
& $ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy $Salida
Pop-Location
Write-Host "Listo: $(Join-Path $Base $Salida)"