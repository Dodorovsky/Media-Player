import sounddevice as sd

# Lista todos los dispositivos disponibles
devices = sd.query_devices()
for i, dev in enumerate(devices):
    print(f"{i}: {dev['name']} ({dev['hostapi']}) - {dev['max_input_channels']} in, {dev['max_output_channels']} out")
