# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import array
import logging
import shutil
import struct
import subprocess

import cherrypy


AUDIO_FORMAT_PCM = 1

class Swift(object):
    def __init__(self):
        self._swift_path = '/usr/local/bin/swift'
        self._aoss_path = '/usr/bin/aoss'

    def tts(self, wave_file, ssml, volume=None):
        if volume is None:
            volume = 100

        bits_per_sample = 16
        bytes_per_sample = bits_per_sample // 8
        num_channels = 1
        sample_rate = 16000

        #
        # Render speech
        #

        audio_params = [
            ('channels'     , num_channels                ),
            ('deadair'      , 1000                        ),
            ('encoding'     , 'pcm%d' % (bits_per_sample,)),
            ('output-format', 'raw'                       ),
            ('sampling-rate', sample_rate                 ),
            ('volume'       , volume                      ),
        ]

        params = ','.join('audio/%s=%s' % (n, v) for n, v in audio_params)

        args = [
            self._aoss_path ,
            self._swift_path,
            '-o', '-'       ,
            '-p',  params   ,
            ssml,
        ]

        samples = array.array('h', subprocess.check_output(args))

        #
        # Compute remaining WAVE field values
        #

        chunk_id = 'RIFF'

        # Header

        # Does not include ChunkID (4) or ChunkSize(4), just Format (4).
        header_size = 4
        subchunk_1_header_size = 8
        subchunk_1_size = 16
        subchunk_2_header_size = 8
        num_samples = len(samples)
        num_blocks = num_samples // num_channels
        subchunk_2_size = num_blocks * num_channels * bytes_per_sample
        chunk_size = (
            header_size
            + subchunk_1_header_size
            + subchunk_1_size
            + subchunk_2_header_size
            + subchunk_2_size
        )

        format = 'WAVE'

        # Subchunk 1

        subchunk_1_id = 'fmt '
        audio_format = AUDIO_FORMAT_PCM
        byte_rate = sample_rate * num_channels * bytes_per_sample
        block_align = num_channels * bytes_per_sample

        # Subchunk 2

        subchunk_2_id = 'data'

        #
        # Write WAVE file
        #

        def write(b):
            if isinstance(b, str):
                b = bytes(b, 'ascii')
            wave_file.write(b)

        def pack(fmt, *values):
            write(struct.pack(fmt, *values))

        # RIFF chunk descriptor
        write(chunk_id)             # ChunkID
        pack('<I', chunk_size)      # ChunkSize (B)
        write(format)               # Format

        # fmt sub-chunk
        write(subchunk_1_id)        # Subchunk1ID
        pack('<I', subchunk_1_size) # Subchunk1Size (B)
        pack('<H', audio_format)    # AudioFormat
        pack('<H', num_channels)    # NumChannels
        pack('<I', sample_rate)     # Samplerate (Hz)
        pack('<I', byte_rate)       # ByteRate (B s^-1)
        pack('<H', block_align)     # BlockAlign (B smaples^-1)
        pack('<H', bits_per_sample) # BitsPerSample (b samples^-1)

        # data sub-chunk
        write(subchunk_2_id)        # Subchunk2ID
        pack('<I', subchunk_2_size) # Subchunk2Size (B)
        samples.tofile(wave_file)   # data

        cherrypy.log(
            '\n'.join([
                'WAVE file metadata'                          ,
                'ChunkID      : {chunk_id}'                   ,
                'ChunkSize    : {chunk_size} B'               ,
                'Format       : {format}'                     ,
                'Subchunk1ID  : {subchunk_1_id}'              ,
                'Subchunk1Size: {subchunk_1_size} B'          ,
                'AudioFormat  : {audio_format}'               ,
                'NumChannels  : {num_channels}'               ,
                'SampleRate   : {sample_rate} Hz'             ,
                'ByteRate     : {byte_rate} B s^-1'           ,
                'BlockAlign   : {block_align} B sample^-1'    ,
                'BitsPerSample: {bits_per_sample} b sample^-1',
                'Subchunk2ID  : {subchunk_2_id}'              ,
                'Subchunk2Size: {subchunk_2_size} B'          ,
            ]).format(**locals()),
            severity=logging.DEBUG,
        )

