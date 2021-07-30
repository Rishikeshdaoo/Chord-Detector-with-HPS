from ChordDetection.chroma_chord_detection import chord_detection, chord_detection_filepath, chord_detection_prefilepath

import numpy as np
import pyaudio # Soundcard audio I/O access library
from tkinter import *
import librosa as lb
import wave

FORMAT = pyaudio.paInt16
CHUNK = 1024
WIDTH = 2
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = 'output.wav'

 
window = Tk()
 
window.title("Chord Detector")
 
window.geometry('400x300')
 
lbl = Label(window, text="Click 'Record' to record your chord for detection")
 
lbl.grid(column=10, row=1)


def clicked():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    lbl.configure(text="Recording...")
    itterations = 0
    chords = []
    print("Recording:")
    if True:
        frames = []

        for i in range(0, int(RATE / CHUNK * 0.2)):
            data = stream.read(CHUNK)
            frames.append(data)

        lbl.configure(text="Recording Completed.")
        lbl.grid(column=12, row=1)

        #stream.stop_stream()
        #stream.close()
        #p.terminate()

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(p.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        chord_name = chord_detection_prefilepath("EE7.wav")
        chord_lbl = Label(window, text=chord_name)
        chord_lbl.grid(column=12, row=10)

        btn.grid(column=12, row=6)
        chords.append(str(chord_name))
        itterations += 1
        if itterations == 13:
            itterations = 0
            print("Estimated chord: " + max(chords, key=chords.count))
            #print(chords)
            chords.clear()


def clicked2():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    lbl.configure(text="Recording...")
    itterations = 0
    chords = []
    print("Recording:")
    while True:
        frames = []

        for i in range(0, int(RATE / CHUNK * 0.2)):
            data = stream.read(CHUNK)
            frames.append(data)

        lbl.configure(text="Recording Completed.")
        lbl.grid(column=12, row=1)

        # stream.stop_stream()
        # stream.close()
        # p.terminate()

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(p.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        chord_name = chord_detection_filepath("output.wav")
        chord_lbl = Label(window, text=chord_name)
        chord_lbl.grid(column=12, row=10)

        btn2.grid(column=12, row=6)
        chords.append(str(chord_name))
        itterations += 1
        if itterations == 13:
            itterations = 0
            print("Estimated chord: " + max(chords, key=chords.count))
            # print(chords)
            chords.clear()


btn = Button(window, text="Record", command=clicked)
# btn2 = Button(window, text="Record live", command=clicked2)
# btn2.grid(column=10, row=6)
btn.grid(column=10, row=6)


window.mainloop()