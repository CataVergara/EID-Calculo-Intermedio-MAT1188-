# Uso: .\render.ps1 -Calidad qh (1080p60) o -Calidad ql (480p15).
param(
  [Alias("Quality")]
  [ValidateSet("ql", "qm", "qh", "qk")]
  [string]$Calidad = "qh",
  [Alias("Output")]
  [string]$Salida = "media/output/MAT1188_EID_G06_2026.mp4"
)

Push-Location $PSScriptRoot
try {
  $python = "python"
  if (Test-Path ".venv/Scripts/python.exe") { $python = ".venv/Scripts/python.exe" }
  elseif (Test-Path ".venv/bin/python") { $python = ".venv/bin/python" }
  & $python render.py --quality $Calidad --output $Salida
  if ($LASTEXITCODE -ne 0) { throw "No se pudo generar el video (código $LASTEXITCODE)." }
}
finally { Pop-Location }
