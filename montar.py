"""Monta los renders 1080p60 con pistas editadas o grabaciones originales."""

import argparse
import csv
from fractions import Fraction
import json
from pathlib import Path
import shutil
import subprocess
import wave

from render import ROOT, concatenate
from utils.edicion import (INSERTOS, RECORTES, duracion_editada,
                          duracion_inserto, insertar_pcm, validar_recortes)
from utils.guion import GUION, DURACION_TOTAL

SR = 48000
FPS = 60


def ffmpeg(args, registro):
    resultado = subprocess.run(
        ["ffmpeg", "-nostdin", "-hide_banner", "-y", *map(str, args)],
        capture_output=True, text=True,
    )
    registro.write_text(resultado.stderr)
    if resultado.returncode:
        raise RuntimeError(f"FFmpeg falló. Revisar {registro}\n{resultado.stderr[-2000:]}")
    return resultado.stderr


def unir(entradas, salida, registro):
    lista = registro.with_suffix(".ffconcat")
    lista.write_text("ffconcat version 1.0\n" + "".join(
        "file '" + str(p.resolve()).replace("'", "'\\''") + "'\n" for p in entradas
    ))
    ffmpeg(["-f", "concat", "-safe", "0", "-i", lista,
            "-c:a", "pcm_s16le", salida], registro)


def preparar_voz(nombre, fuente, destino, trabajo):
    escenas = [e for e, (_, voz) in GUION.items() if voz == nombre and e in RECORTES
               and (not isinstance(fuente, dict) or e in fuente)]
    recortados = []
    for escena in escenas:
        original = fuente[escena] if isinstance(fuente, dict) else fuente
        piezas = []
        for i, (inicio, fin) in enumerate(RECORTES[escena]):
            pieza = trabajo / f"{escena}_{i}_toma.wav"
            duracion = fin - inicio
            ffmpeg(["-i", original, "-map", "0:a:0", "-vn", "-af",
                    f"atrim=start={inicio}:end={fin},asetpts=PTS-STARTPTS,highpass=f=65,"
                    f"afade=t=in:d=0.012,afade=t=out:st={duracion-0.012:.6f}:d=0.012",
                    "-ar", SR, "-ac", "2", "-c:a", "pcm_s16le", pieza],
                   trabajo / f"{escena}_{i}_toma.log")
            with wave.open(str(pieza)) as audio:
                if audio.getnframes() != round(duracion * SR):
                    raise ValueError(f"Grabación incompleta para {escena}: {original}")
            piezas.append(pieza)
        recortado = trabajo / f"{escena}_recorte.wav"
        unir(piezas, recortado, trabajo / f"{escena}_unir.log")
        if escena in INSERTOS:
            with wave.open(str(recortado)) as audio:
                parametros = audio.getparams()
                contenido = audio.readframes(audio.getnframes())
            insertos = []
            for inserto in INSERTOS[escena]:
                duracion = duracion_inserto(inserto)
                agregado = bytes(round(duracion * SR) * 4)
                insertos.append((inserto["posicion"], agregado))
            contenido = insertar_pcm(contenido, insertos, SR, 4)
            with wave.open(str(recortado), "wb") as audio:
                audio.setparams(parametros)
                audio.writeframes(contenido)
        recortados.append(recortado)
    corta = nombre.split()[0]
    bruto = trabajo / f"{corta}_voz.wav"
    unir(recortados, bruto, trabajo / f"{corta}_unir.log")
    informe = ffmpeg(["-i", bruto, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                      "-f", "null", "-"], trabajo / f"{corta}_medicion.log")
    medidas, _ = json.JSONDecoder().raw_decode(informe[informe.rfind("{"):])
    filtro = (
        "loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:print_format=json:"
        f"measured_I={medidas['input_i']}:measured_TP={medidas['input_tp']}:"
        f"measured_LRA={medidas['input_lra']}:measured_thresh={medidas['input_thresh']}:"
        f"offset={medidas['target_offset']}"
    )
    normalizado = trabajo / f"{corta}_normalizado.wav"
    ffmpeg(["-i", bruto, "-af", filtro, "-ar", SR, "-ac", "2",
            "-c:a", "pcm_s16le", normalizado], trabajo / f"{corta}_normalizacion.log")
    offset = 0
    salidas = {}
    for escena in escenas:
        muestras = round(duracion_editada(escena, RECORTES[escena]) * SR)
        total = round(GUION[escena][0] * SR)
        numero = list(GUION).index(escena) + 1
        salida = destino / f"{numero:02d}_{escena}_{corta}.wav"
        ffmpeg(["-i", normalizado, "-af",
                f"atrim=start_sample={offset}:end_sample={offset+muestras},asetpts=PTS-STARTPTS,"
                f"apad=whole_len={total},atrim=end_sample={total}",
                "-ar", SR, "-ac", "2", "-c:a", "pcm_s16le", salida],
               trabajo / f"{escena}_voz.log")
        offset += muestras
        salidas[escena] = salida
    unir(salidas.values(), destino / f"{corta}_voz_editada.wav", trabajo / f"{corta}_final.log")
    return salidas


def verificar_videos(carpeta):
    """Rechaza renders viejos antes de unirlos con las nuevas voces."""
    for escena, (duracion, _) in GUION.items():
        archivo = carpeta / f"{escena}.mp4"
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height,r_frame_rate,nb_frames", "-of", "json", str(archivo)],
            capture_output=True, text=True, check=True,
        )
        stream = json.loads(result.stdout)["streams"][0]
        if (stream["width"], stream["height"]) != (1920, 1080) or Fraction(stream["r_frame_rate"]) != FPS:
            raise ValueError(f"{escena}: se necesita el render 1080p60.")
        if int(stream["nb_frames"]) != round(duracion * FPS):
            raise ValueError(f"{escena}: render desactualizado. Ejecutar python render.py --quality qh.")


def validar_audios_editados(carpeta):
    """Exige las diez pistas completas para conservar los cortes ya aprobados."""
    pistas = {}
    for numero, (escena, (duracion, voz)) in enumerate(GUION.items(), 1):
        archivo = carpeta / f"{numero:02d}_{escena}_{voz.split()[0]}.wav"
        with wave.open(str(archivo)) as audio:
            muestras = round(duracion * SR)
            if (audio.getnchannels(), audio.getsampwidth(), audio.getframerate(),
                    audio.getnframes()) != (1, 2, SR, muestras):
                raise ValueError(f"{archivo.name}: se necesita PCM mono de 16 bits, "
                                 f"48 kHz y {duracion} segundos.")
            if len(audio.readframes(muestras)) != muestras * 2:
                raise ValueError(f"{archivo.name}: el archivo de audio está incompleto.")
        pistas[escena] = archivo
    return pistas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audios-editados", type=Path,
                        help="Carpeta con los diez WAV finales de CapCut, sin volver a editarlos.")
    parser.add_argument("--catalina", type=Path)
    parser.add_argument("--ignacio", type=Path)
    for parte in ("refinamiento", "comparacion", "respuesta", "creditos"):
        parser.add_argument(f"--marcelo-{parte}", type=Path)
    parser.add_argument("--videos", type=Path, default=ROOT / "media/videos/escenas/1080p60")
    parser.add_argument("--salida", type=Path, default=ROOT / "media/output/montaje")
    parser.add_argument("--solo-audio", action="store_true")
    args = parser.parse_args()
    grabaciones = [args.catalina, args.ignacio, args.marcelo_refinamiento,
                   args.marcelo_comparacion, args.marcelo_respuesta, args.marcelo_creditos]
    if args.audios_editados and any(grabaciones):
        parser.error("Elegir --audios-editados o las grabaciones originales, sin combinarlos.")
    if not args.audios_editados and not (args.catalina and args.ignacio):
        parser.error("Indicar --audios-editados o las grabaciones --catalina y --ignacio.")
    validar_recortes()
    for programa in ("ffmpeg", "ffprobe"):
        if shutil.which(programa) is None:
            raise RuntimeError(f"Se necesita {programa} en el PATH.")
    fuentes = {} if args.audios_editados else {
        "Catalina Vergara": args.catalina.resolve(), "Ignacio De Celis": args.ignacio.resolve(),
    }
    marcelo = {escena: archivo.resolve() for escena, archivo in (
        ("Refinamiento", args.marcelo_refinamiento),
        ("ComparacionFinal", args.marcelo_comparacion),
        ("RespuestaCentral", args.marcelo_respuesta),
        ("Creditos", args.marcelo_creditos),
    ) if archivo is not None}
    if marcelo:
        fuentes["Marcelo Santana"] = marcelo
    originales = [archivo for fuente in fuentes.values()
                  for archivo in (fuente.values() if isinstance(fuente, dict) else (fuente,))]
    salida = args.salida.resolve()
    editados = args.audios_editados.resolve() if args.audios_editados else None
    if editados and (editados.is_relative_to(salida) or salida.is_relative_to(editados)):
        raise ValueError("La carpeta de salida debe estar separada de los audios editados.")
    for fuente in (*originales, args.videos.resolve()):
        if fuente.is_relative_to(salida):
            raise ValueError("La carpeta de salida debe estar separada de los originales.")
    for fuente in originales:
        if not fuente.is_file():
            raise FileNotFoundError(fuente)
    if not args.solo_audio:
        verificar_videos(args.videos)
    finales = validar_audios_editados(editados) if editados else {}
    trabajo, audios = salida / "intermedios", salida / "Audios"
    for carpeta in (trabajo, audios):
        carpeta.mkdir(parents=True, exist_ok=True)
    pistas = {}
    for escena, archivo in finales.items():
        destino = audios / archivo.name
        shutil.copy2(archivo, destino)
        pistas[escena] = destino
    if finales:
        for voz in dict.fromkeys(voz for _, voz in GUION.values()):
            corta = voz.split()[0]
            unir([pistas[e] for e, (_, persona) in GUION.items() if persona == voz],
                 audios / f"{corta}_voz_editada.wav", trabajo / f"{corta}_final.log")
    for nombre, fuente in fuentes.items():
        print(f"Preparando {nombre}...", flush=True)
        pistas.update(preparar_voz(nombre, fuente, audios, trabajo))
    disponibles = set(pistas)
    pendientes = [escena for escena in GUION if escena not in disponibles]
    for i, (escena, (duracion, _)) in enumerate(GUION.items(), 1):
        if escena not in pistas:
            archivo = trabajo / f"{i:02d}_{escena}_voz_pendiente.wav"
            ffmpeg(["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", duracion,
                    "-c:a", "pcm_s16le", archivo], trabajo / f"{escena}_silencio.log")
            pistas[escena] = archivo
    for escena, archivo in pistas.items():
        with wave.open(str(archivo)) as audio:
            if audio.getnframes() != round(GUION[escena][0] * SR):
                raise ValueError(f"Duración de audio incorrecta: {escena}")
    track = audios / "Voces_alineadas_desde_cero.wav"
    unir([pistas[e] for e in GUION], track, trabajo / "voces_alineadas.log")
    with (salida / "Tiempos_CapCut.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Escena", "Voz", "Inicio_segundos", "Duracion_segundos", "Grabacion"])
        inicio = 0
        for escena, (duracion, voz) in GUION.items():
            writer.writerow([escena, voz, round(inicio, 3), duracion,
                             "disponible" if escena in disponibles else "pendiente"])
            inicio += duracion
    if args.solo_audio:
        print(f"Audios preparados: {audios}")
        return
    base = salida / "Video_sin_audio_CapCut.mp4"
    concatenate(args.videos.resolve(), base)
    clips = salida / "Escenas_para_CapCut"
    clips.mkdir(exist_ok=True)
    for i, escena in enumerate(GUION, 1):
        shutil.copy2(args.videos / f"{escena}.mp4", clips / f"{i:02d}_{escena}.mp4")
    final = salida / ("BORRADOR_faltan_voces.mp4" if pendientes else "MAT1188_EID_G06_2026.mp4")
    ffmpeg(["-i", base, "-i", track, "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", SR, "-ac", "1",
            "-t", DURACION_TOTAL, "-movflags", "+faststart", final], trabajo / "montaje.log")
    print(f"Montaje generado: {final}")
    if pendientes:
        print("Faltan grabaciones: " + ", ".join(pendientes))


if __name__ == "__main__":
    main()
