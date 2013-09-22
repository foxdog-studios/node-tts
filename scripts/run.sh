#!/bin/bash

set -o errexit
set -o nounset

repo=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/..")
cd -- "${repo}"

set +o nounset
source env3/bin/activate
set -o nounset

export PYTHONPATH="${PYTHONPATH-}:${repo}/src"

if [[ $# == 0 ]]; then
    args=(
        --bpm 90
        --config "${repo}/config.yaml"
        --host "$(hostname -i)"
        --output build
        --words /usr/share/dict/cracklib-small
        phonemes.pkl
        backing_tracks/default.wav
        melodies/default.txt
    )
else
    args=( "$@" )
fi

python -m tts "${args[@]}"

