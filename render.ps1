# Script para renderizar y unir escenas (Manim + FFmpeg)
# Uso: .\render.ps1  (desde PowerShell, en esta carpeta)

param(
  [string]$Quality = "1080p15",  # ql, qk, qh, 480p15, 720p30, 1080p15, etc.
  [string]$Output  = "VIDEO_FINAL.mp4"
)

$Base = ".\media\videos\escenas\$Quality"
if (-not (Test-Path $Base)) {
  Write-Host "No existe $Base. Se intentara renderizar en $Quality..."
  python -m manim render -$Quality.Replace('p','').Replace('1','').Replace('3','') escenas.py 2>$null
}

$files = Get-ChildItem -Path $Base -Filter "*.mp4" -File | Sort-Object Name
if ($files.Count -eq 0) {
  Write-Host "No hay archivos .mp4 en $Base. Renderizando todas las escenas con -$($Quality)..."
  python -m manim render -q escenas.py
  $files = Get-ChildItem -Path $Base -Filter "*.mp4" -File | Sort-Object Name
}

$concat = Join-Path $Base "concat_list.txt"
$files | ForEach-Object { "file '$($_.FullName.Replace('\','/'))'" } | Set-Content $concat

$ffmpeg = python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"
& $ffmpeg -f concat -safe 0 -i $concat -c copy (Join-Path $Base $Output)
Write-Host "Listo: $Output en $Base"