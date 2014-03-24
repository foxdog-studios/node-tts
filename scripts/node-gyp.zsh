#!/usr/bin/env zsh

setopt ERR_EXIT
setopt NO_UNSET

cd -- ${0:h}/..

exec node-gyp --python=/usr/bin/python2.7 $@

