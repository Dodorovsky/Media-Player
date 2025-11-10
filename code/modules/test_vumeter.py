from pydub import AudioSegment
from pydub.utils import which

print("FFmpeg detectado en:", which("ffmpeg"))

audio = AudioSegment.from_file("C:/Users/dodor/OneDrive/Desktop/Planet.mp3")  # Cambiá la ruta si es necesario

print("Duración (ms):", len(audio))
print("Volumen RMS:", audio.rms)

