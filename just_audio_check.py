import wave

# Buka file WAV
with wave.open(r'D:\Work\python-sip\1.wav', 'rb') as f:
    frames = f.getnframes()
    print("Total frames:", frames)
    sample_width = f.getsampwidth()
    print("Sample width:", sample_width, "bytes")
    frame_rate = f.getframerate()
    print("Frame rate:", frame_rate, "Hz")
    num_channels = f.getnchannels()
    print("Channels:", num_channels)

    data = f.readframes(160)
    print("Partial frame data:", data[:100])  

if set(data) == {0}:
    print("The audio data contains only silence (zeros).")
else:
    print("The audio data contains non-zero values.")


print("\n")

print("\n")

print("\n")

import wave

with wave.open(r'D:\Work\python-sip\1.wav', 'rb') as f:
    chunk_size = 160 
    frames = f.getnframes()
    print("Total frames:", frames)

    # Baca sebagian data
    for i in range(0, frames, chunk_size):
        data = f.readframes(chunk_size)
        print("Frame data:", data[:100])  

        if set(data) != {0}:
            print("Non-silence audio data found.")
            break
