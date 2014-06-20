#!/usr/bin/env zsh

setopt ERR_EXIT
setopt NO_UNSET

cd -- $0:h:h
npm install
npm test
aplay --channels=1 --format=S16_LE --rate=16000  /tmp/tts.pcm
rm /tmp/tts.pcm

