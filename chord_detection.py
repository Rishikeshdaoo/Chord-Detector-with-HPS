from ChordDetection.chroma_chord_detection import chord_detection, chord_detection_filepath

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
 
window.geometry('200x120')
 
lbl = Label(window, text="Click 'Record' to record your chord for detection")
 
lbl.grid(column=10, row=1)
 
def clicked():

    p = pyaudio.PyAudio()

    lbl.configure(text="Recording...")

    stream = p.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    lbl.configure(text="Recording Completed.")
    lbl.grid(column=12, row=1)

    stream.stop_stream()
    stream.close()
    p.terminate()
 
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    chord_name = chord_detection_filepath("./output.wav")

    chord_lbl = Label(window, text=chord_name)
    chord_lbl.grid(column=12, row=10)
 
    btn.grid(column=12, row=6)

    print("Estimated chord: " + str(chord_name))
 
btn = Button(window, text="Record", command=clicked)
btn.grid(column=10, row=6)

window.mainloop()