#!/usr/bin/env zsh

setopt -o err_exit
setopt -o no_unset

repo=$(realpath -- ${0:h}/..)

unsetopt no_unset
source $repo/env/bin/activate
setopt no_unset

exec python tools/dino_control.py  $@

