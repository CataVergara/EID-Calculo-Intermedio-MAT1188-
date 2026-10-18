"""Las pistas finales se conservan y los archivos incompletos se rechazan."""

from pathlib import Path
import tempfile
import unittest
import wave

from montar import SR, validar_audios_editados
from utils.guion import GUION


class MontajeFinalTest(unittest.TestCase):
    def test_admite_las_diez_pistas_y_rechaza_una_faltante(self):
        with tempfile.TemporaryDirectory() as directorio:
            carpeta = Path(directorio)
            for numero, (escena, (duracion, voz)) in enumerate(GUION.items(), 1):
                archivo = carpeta / f"{numero:02d}_{escena}_{voz.split()[0]}.wav"
                with wave.open(str(archivo), "wb") as audio:
                    audio.setparams((1, 2, SR, 0, "NONE", "not compressed"))
                    audio.writeframes(bytes(round(duracion * SR) * 2))
            pistas = validar_audios_editados(carpeta)
            self.assertEqual(list(pistas), list(GUION))
            pistas["RespuestaCentral"].unlink()
            with self.assertRaises(FileNotFoundError):
                validar_audios_editados(carpeta)

    def test_rechaza_canal_duracion_y_pcm_incompleto(self):
        with tempfile.TemporaryDirectory() as directorio:
            carpeta = Path(directorio)
            archivo = carpeta / "01_Portada_Catalina.wav"
            muestras = round(GUION["Portada"][0] * SR)
            for canales, longitud in ((2, muestras), (1, muestras - 1)):
                with self.subTest(canales=canales, longitud=longitud):
                    with wave.open(str(archivo), "wb") as audio:
                        audio.setparams((canales, 2, SR, 0, "NONE", "not compressed"))
                        audio.writeframes(bytes(longitud * canales * 2))
                    with self.assertRaisesRegex(ValueError, "PCM mono"):
                        validar_audios_editados(carpeta)
            with wave.open(str(archivo), "wb") as audio:
                audio.setparams((1, 2, SR, 0, "NONE", "not compressed"))
                audio.writeframes(bytes(muestras * 2))
            with archivo.open("r+b") as audio:
                audio.truncate(archivo.stat().st_size - 2)
            with self.assertRaisesRegex(ValueError, "incompleto"):
                validar_audios_editados(carpeta)
