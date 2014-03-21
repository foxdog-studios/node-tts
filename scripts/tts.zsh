#!/usr/bin/env zsh

setopt -o ERR_EXIT
setopt -o NO_UNSEt

repo=$(realpath -- ${0:h}/..)

if (( ! $+TTS_CONFIG )); then
    export TTS_CONFIG=$repo/local/config/default/tts.yaml
fi

unsetopt NO_UNSET
source $repo/local/venv/bin/activate
setopt NO_UNSET

export PYTHONPATH=${PYTHONPATH:+$PYTHONPATH:}$repo
exec python -m tts $@

