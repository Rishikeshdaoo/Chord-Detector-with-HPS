import json
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
from ChordDetection.chromagram import extract_pitch_chroma, block_audio, compute_stft, file_read, file_normalize

# Loading the JSON into a variable
with open('chord_template.json', 'r') as fp:
    templates_json = json.load(fp)

# List of the 24 (major and minor) chord classes
chords = ['N', 'G maj', 'G# maj', 'A maj', 'A# maj', 'B maj', 'C maj', 'C# maj',
            'D maj','D# maj','E maj', 'E7', 'F maj','F# maj','G min','G# min','A min',
            'A# min','B min','C min','C# min','D min','D# min','E min','F min','F# min']

templates = []

# Setting the block size, hop size for windowing signal and reference frequency for calculating PCP
block_size = 8192
hop_size = 1024

reference_frequency = 440


def chord_detection(audio):

    fs = 44100

    for chord in chords:
        if chord == 'N':
            continue
        templates.append(templates_json[chord])
    print(templates)

    x = file_normalize(audio)

    xb, _ = block_audio(x, block_size, hop_size, fs)

    X, fs = compute_stft(xb, fs, block_size, hop_size)

    chroma = extract_pitch_chroma(X, fs, reference_frequency)

    chroma_template = np.mean(chroma, axis=1)

    """Correlate 12D chroma vector with each of 24 major and minor chords"""
    cor_vec = np.zeros(24)
    for idx in range(24):
        cor_vec[idx] = np.dot(chroma_template, np.array(templates[idx]))
    idx_max_cor = np.argmax(cor_vec)

    idx_chord = int(idx_max_cor + 1)
    chord_name = tuple(chords[idx_chord].split(" "))

    # # Plotting all figures
    # plt.figure(1)
    # notes = ['G','G#','A','A#','B','C','C#','D','D#','E','F','F#']
    # plt.xticks(np.arange(12),notes)
    # plt.title('Pitch Class Profile')
    # plt.xlabel('Notes')
    # plt.ylim((0.0,1.0))
    # plt.grid(True)
    # plt.plot(notes, chroma_template)
    # plt.show()

    return chord_name


def chord_detection_filepath(filepath):

    for chord in chords:
        if chord == 'N':
            continue
        templates.append(templates_json[chord])

    fs, x = file_read(filepath)
    if len(x.shape) > 1:
        x = x[:, 1]




    xb, t = block_audio(x, block_size, hop_size, fs)
    X, fs = compute_stft(xb, fs, block_size, hop_size)

    chroma = extract_pitch_chroma(X, fs, reference_frequency)

    print('-----------------------------------')
    # print(chroma)
    chroma_template = np.mean(chroma, axis=1)
    print('')
    for i in range(len(chroma_template)):
        if chroma_template[i] < 0.05:
            chroma_template[i] = 0
    print(chroma_template)

    """Correlate 12D chroma vector with each of 24 major and minor chords"""
    cor_vec = np.zeros(24)
    for idx in range(24):
        cor_vec[idx] = np.dot(chroma_template, np.array(templates[idx]))
    print(cor_vec)
    idx_max_cor = np.argmax(cor_vec)
    #print(idx_max_cor)

    idx_chord = int(idx_max_cor + 1)
    chord_name = tuple(chords[idx_chord].split(" "))
    # print(chord_name)
    # # Plotting all figures
    # plt.figure(1)
    # notes = ['G','G#','A','A#','B','C','C#','D','D#','E','F','F#']
    # plt.xticks(np.arange(12),notes)
    # plt.title('Pitch Class Profile')
    # plt.xlabel('Notes')
    # plt.ylim((0.0,1.0))
    # plt.grid(True)
    # plt.plot(notes, chroma_template)
    # plt.show()

    return chord_name


def chord_detection_prefilepath(filepath):

    for chord in chords:
        if chord == 'N':
            continue
        templates.append(templates_json[chord])

    fs, x = file_read(filepath)
    if len(x.shape) > 1:
        x = x[:, 1]
    xb, t = block_audio(x, block_size, hop_size, fs)
    for i in range(0, len(xb) - 80, 80):
        X, fs = compute_stft(xb[i:i+80], fs, block_size, hop_size)

        chroma = extract_pitch_chroma(X, fs, reference_frequency)
        print('-----------------------------------')
        #print(chroma)
        chroma_template = np.mean(chroma, axis=1)
        for i in range(len(chroma_template)):
            if chroma_template[i] < 0.07:
                chroma_template[i] = 0
        print('')
        print(chroma_template)
        """Correlate 12D chroma vector with each of 24 major and minor chords"""
        cor_vec = np.zeros(25)
        for idx in range(25):
            cor_vec[idx] = np.dot(chroma_template, np.array(templates[idx]))
        print(templates)
        print(cor_vec)
        idx_max_cor = np.argmax(cor_vec)
        idx_chord = int(idx_max_cor + 1)
        chord_name = tuple(chords[idx_chord].split(" "))
        print(chord_name)
        # # Plotting all figures
        # plt.figure(1)
        # notes = ['G','G#','A','A#','B','C','C#','D','D#','E','F','F#']
        # plt.xticks(np.arange(12),notes)
        # plt.title('Pitch Class Profile')
        # plt.xlabel('Notes')
        # plt.ylim((0.0,1.0))
        # plt.grid(True)
        # plt.plot(notes, chroma_template)
        # plt.show()

    return chord_name


if __name__ == "__main__":
    count = 0

    folderpath = "/Users/marketinggramusic/Documents/Sem1/MIR/Project/crs/single-chord-dataset/"

    for folder in listdir(folderpath):
        if folder != ".DS_Store":
            filepath = os.path.join(folderpath, folder)
            if filepath != ".DS_Store":
                for file in listdir(filepath):
                    if file != ".DS_Store":
                        file_path = os.path.join(filepath,file)
                        chord = chord_detection_filepath(file_path)
                        print("Estimated: " + str(chord) + "    |    " + "Ground Truth: " + folder)
                        # est = str(chord[0]) + " " + str(chord[1])