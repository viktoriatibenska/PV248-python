import sys
import numpy as np
import wave
import struct
from statistics import mean

def main(audioFile):
    f = wave.open(audioFile, 'r')
    frameRate = f.getframerate()
    dataSize = f.getnframes()
    nChannels = f.getnchannels()
    
    if f.getsampwidth() == 2:
        fmt = "<i2"
    else :
        fmt = "<i4"

    window = 0
    maxFreq = -1
    minFreq = -1
    while (window < int(dataSize / frameRate)):
        data = f.readframes(frameRate)
        data = np.frombuffer(data, dtype=fmt)
        if nChannels == 2 :
            data = data.reshape(-1, nChannels)
            data = data.sum(axis=1) / 2

        frequencies = abs(np.fft.rfft(data) / frameRate)
        average = mean(frequencies)

        for value, freq in enumerate(frequencies):
            if freq > 20 * average:
                if maxFreq == -1 and minFreq == -1:
                    maxFreq = value
                    minFreq = value
                if value > maxFreq:
                    maxFreq = value
                if value < minFreq:
                    minFreq = value

        window += 1
    
    f.close()

    if maxFreq == -1 and minFreq == -1:
        print("no peaks")
    else:
        print("low = " + str(minFreq) + ", high = " + str(maxFreq))

if __name__ == "__main__":
    main(sys.argv[1])
