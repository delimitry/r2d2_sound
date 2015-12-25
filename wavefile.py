#!/usr/bin/env python
#-*- coding: utf8 -*-
#-----------------------------------------------------------------------
# Author: delimitry
#-----------------------------------------------------------------------

import struct


class WaveFile(object):
    """
    Wave file worker class
    """

    def __init__(self, sample_rate):
        self.subchunk_size = 16   # subchunk data size (16 for PCM)
        self.compression_type = 1 # compression (PCM = 1 [linear quantization])
        self.channels_num = 1     # channels (mono = 1, stereo = 2)
        self.bits_per_sample = 16
        self.block_alignment = self.channels_num * self.bits_per_sample / 8
        self.sample_rate = sample_rate
        self.byte_rate = self.sample_rate * self.channels_num * self.bits_per_sample / 8
        self.duration = 0
        self.data = []

    def add_data_subchunk(self, duration, data):
        self.duration += duration
        self.data += data

    def save(self, filename):
        self.samples_num = int(self.duration * self.sample_rate)
        self.subchunk2_size = self.samples_num * self.channels_num * self.bits_per_sample / 8
        with open(filename, 'wb') as f:
            # write RIFF header
            f.write('RIFF')
            f.write(struct.pack('<i', 4 + (8 + self.subchunk_size) + (8 + self.subchunk2_size)))
            f.write('WAVE')
            # write fmt subchunk
            f.write('fmt ')                                     # chunk type
            f.write(struct.pack('<i', self.subchunk_size))      # data size
            f.write(struct.pack('<h', self.compression_type))   # compression type
            f.write(struct.pack('<h', self.channels_num))       # channels
            f.write(struct.pack('<i', self.sample_rate))        # sample rate
            f.write(struct.pack('<i', self.byte_rate))          # byte rate
            f.write(struct.pack('<h', self.block_alignment))    # block alignment
            f.write(struct.pack('<h', self.bits_per_sample))    # sample depth
            # write data subchunk
            f.write('data')
            f.write(struct.pack ('<i', self.subchunk2_size))
            for d in self.data:
                sound_data = struct.pack('<h', d)
                f.write(sound_data)
