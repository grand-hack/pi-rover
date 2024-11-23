import pyaudio
import numpy as np

SAMPLE_RATE = 48000
DURATION = 3
FREQUENCY = 440
AMPLITUDE = 0.5
#CHUNK = 1024  # Number of frames per buffer
CHUNK = 10

t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), False)
samples = (AMPLITUDE * 32767 * np.sin(2 * np.pi * FREQUENCY * t)).astype(np.int16)

p = pyaudio.PyAudio()

stream = p.open(
    output_device_index=0,
    format=pyaudio.paInt16,
    channels=1,
    rate=SAMPLE_RATE,
    output=True,
    frames_per_buffer=CHUNK
)

# Play in chunks
for i in range(0, len(samples), CHUNK):
    chunk = samples[i:i + CHUNK]
    print ("-->", chunk.tobytes())
    stream.write(chunk.tobytes())

stream.stop_stream()
stream.close()
p.terminate()
