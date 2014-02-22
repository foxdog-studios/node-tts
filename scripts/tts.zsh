#!/usr/bin/env zsh

setopt -o err_exit
setopt -o no_unset

repo=$(realpath -- ${0:h}/..)

if (( ! $+TTS_CONFIG )); then
    export TTS_CONFIG=$repo/local/config/default/tts.yaml
fi

unsetopt no_unset
source $repo/env/bin/activate
setopt no_unset

export PYTHONPATH=${PYTHONPATH:+$PYTHONPATH:}$repo
exec python -m tts $@

