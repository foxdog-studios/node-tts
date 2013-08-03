#!/bin/bash

set -o errexit
set -o nounset

REPO=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/..")
cd -- "${REPO}"

set +o nounset
source env/bin/activate
set -o nounset

export PYTHONPATH="${PYTHONPATH-}:${REPO}/src"

if [[ $# == 0 ]]; then
    args=(
        --bpm 90
        --log-level debug
        backing_tracks/default.wav
        melodies/default.txt
    )
else
    args=( "$@" )
fi

python -m tts "${args[@]}"

