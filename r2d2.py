#!/usr/bin/env python
#-*- coding: utf8 -*-
#-----------------------------------------------------------------------
# Author: delimitry
#-----------------------------------------------------------------------

import math
import random
import winsound
from wavefile import WaveFile


note_freqs = [
#  C       C#       D      D#      E       F       F#      G       G#      A       A#      B   
 16.35,  17.32,  18.35,  19.45,   20.6,  21.83,  23.12,   24.5,  25.96,   27.5,  29.14,  30.87,
  32.7,  34.65,  36.71,  38.89,   41.2,  43.65,  46.25,   49.0,  51.91,   55.0,  58.27,  61.74,
 65.41,   69.3,  73.42,  77.78,  82.41,  87.31,   92.5,   98.0,  103.8,  110.0,  116.5,  123.5,
 130.8,  138.6,  146.8,  155.6,  164.8,  174.6,  185.0,  196.0,  207.7,  220.0,  233.1,  246.9,
 261.6,  277.2,  293.7,  311.1,  329.6,  349.2,  370.0,  392.0,  415.3,  440.0,  466.2,  493.9,
 523.3,  554.4,  587.3,  622.3,  659.3,  698.5,  740.0,  784.0,  830.6,  880.0,  932.3,  987.8,
1047.0, 1109.0, 1175.0, 1245.0, 1319.0, 1397.0, 1480.0, 1568.0, 1661.0, 1760.0, 1865.0, 1976.0,
2093.0, 2217.0, 2349.0, 2489.0, 2637.0, 2794.0, 2960.0, 3136.0, 3322.0, 3520.0, 3729.0, 3951.0,
4186.0, 4435.0, 4699.0, 4978.0, 5274.0, 5588.0, 5920.0, 6272.0, 6645.0, 7040.0, 7459.0, 7902.0,
]


def generate_sin_wave(sample_rate, frequency, duration, amplitude):
    """
    Generate a sinusoidal wave based on `sample_rate`, `frequency`, `duration` and `amplitude`
    `frequency` in Hertz, `duration` in seconds, the values of `amplitude` must be in range [0..1]
    """
    data = []
    samples_num = int(duration * sample_rate)
    volume = amplitude * 32767
    for n in xrange(samples_num):
        value = math.sin(2 * math.pi * n * frequency / sample_rate)
        data.append(int(value * volume))
    return data


def generate_r2d2_message(filename):
    """
    Generate R2D2 message and save to `filename`
    """
    min_msg_len = 1
    max_msg_len = 20
    r2d2_message = []
    for _ in range(random.randint(min_msg_len, max_msg_len)):
        r2d2_message.append(note_freqs[random.randint(0, len(note_freqs) - 1)])

    sample_rate = 8000  # 8000 Hz
    dot_dur = 0.080  # 80 ms
    volume = 0.80  # 80%

    wave = WaveFile(sample_rate)
    wave_duration = 0
    wave_data = []
    for freq in r2d2_message:
        wave_duration += dot_dur
        wave_data += generate_sin_wave(sample_rate, freq, dot_dur, volume)
    wave.add_data_subchunk(wave_duration, wave_data)
    wave.save(filename)


def main():
    filename = 'r2d2.wav'
    generate_r2d2_message(filename)

    # play R2D2 message
    winsound.PlaySound(filename, winsound.SND_FILENAME)


if __name__ == '__main__':
    main()
