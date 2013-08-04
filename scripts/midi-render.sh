#!/bin/bash

set -o errexit
set -o nounset

usage()
{
    echo '
    Render a MIDI file to WAV

    Usage:

        # midi-render.sh INPUT_MIDI OUTPUT_WAV
    '
    exit 1
}

if [[ $# != 2 ]]; then
    usage
fi

input_midi="${1}"
ouput_wav="${2}"

fluidsynth --audio-file-type wav                       \
           --disable-lash                              \
           --fast-render "${2}"                        \
           --no-midi-in                                \
           --no-shell                                  \
           -o synth.cpu-cores=2                        \
           --sample-rate 16000                         \
           /usr/share/soundfonts/fluidr3/FluidR3GM.SF2 \
           "${1}"

