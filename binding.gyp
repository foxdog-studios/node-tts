{
  "targets": [{
    "target_name": "tts",
    "sources": [
      "src/tts.cc",
      "src/tts_wrap.cc"
    ],
    "include_dirs": [
      "src"
    ],
    "libraries": [
      "-lceplang_en",
      "-lceplex_us",
      "-lswift"
    ]
  }]
}

