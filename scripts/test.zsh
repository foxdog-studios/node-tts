#!/usr/bin/env zsh

cd -- ${0:h}/..
exec aoss coffee <<-'EOF'
	fs = require 'fs'
	tts = require './build/Release/tts'
	t = new tts.Tts()
	w = t.createWaveform 'Hello, World!'
	fs.writeFileSync '/tmp/tts.pcm', w
EOF

