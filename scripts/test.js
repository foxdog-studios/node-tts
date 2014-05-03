(function () {
  'use strict';
  var TTS = require('../build/Release/tts');
  var tts = new TTS.Tts();
  var fs = require('fs');
  fs.writeFileSync('/tmp/lexicon.txt', 'hello 0  k eh1 p s t r ah0 l');
  tts.tryLoadLexicon("/tmp/lexicon.txt");
  var pcm = tts.createWaveform('Hello, World!');
  fs.writeFileSync('/tmp/tts.pcm', pcm);
}());

