import array
import shutil
import struct
import subprocess

class Swift:
    def __init__(self, swift_path, threshold=0.2):
        self._swift_path = swift_path
        self._threshold = threshold

    def tts(self, ssml):
        subprocess.check_call((shutil.which('aoss'), self._swift_path, ssml))

    def tts_file(self, ssml, output_path, volume=100):
        bits_per_sample = 16
        bytes_per_sample = bits_per_sample // 8
        num_channels = 1
        sample_rate = 16000

        samples = array.array('h', subprocess.check_output((
            shutil.which('aoss'),
            self._swift_path,
            '-o', '-',
            '-p',
                'audio/channels=%s,'
                'audio/deadair=1000,'
                'audio/encoding=pcm%s,'
                'audio/output-format=raw,'
                'audio/sampling-rate=%s,'
                'audio/volume=%s'
                    % (num_channels, bits_per_sample, sample_rate, volume),
            ssml)))

        num_samples = len(samples)
        num_blocks = num_samples // num_channels
        subchunk_2_size = num_blocks * num_channels * bytes_per_sample

        with open(output_path, 'wb') as f:
            f.write(b'RIFF') # Chunk ID

            # Bytes to follow
            f.write(struct.pack('<I', 36 + subchunk_2_size))

            f.write(b'WAVEfmt ') # Sub chunk ID

            f.write(struct.pack('<I', 16)) # Byte to follow in sub chunk

            f.write(struct.pack('<H', 1)) # Audio format: PCM

            f.write(struct.pack('<H', num_channels)) # Channels: Mono

            f.write(struct.pack('<I', sample_rate)) # Sample rate (Hz)

            f.write(struct.pack('<I', sample_rate * num_channels * bytes_per_sample))

            f.write(struct.pack('<H', num_channels * bytes_per_sample))

            f.write(struct.pack('<H', bits_per_sample)) # Bits per sample

            f.write(b'data') # Subchunk ID

            # Subchunk 2 size
            f.write(struct.pack('<I', subchunk_2_size))

            # Data
            samples.tofile(f)

        start_sample = 0
        previous_sample = 0
        threshold = (2 ** 16 / 2) * self._threshold
        for i, sample in enumerate(samples):
            if previous_sample < 0 and sample >= 0 \
            or previous_sample >= 0 and sample < 0:
                start_sample = i
            if abs(sample) > threshold:
                break
            previous_sample = sample

        return -start_sample / sample_rate



