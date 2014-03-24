#ifndef TTS_TTS_WRAP_H_
#define TTS_TTS_WRAP_H_

#include <node.h>
#include <v8.h>

#include "tts.h"

namespace tts {

void Init(v8::Handle<v8::Object> exports);

class TtsWrap : public node::ObjectWrap {
 public:
  static void Init(v8::Handle<v8::Object> exports);

 private:
  static v8::Persistent<v8::Function> constructor;

  Tts tts_;

  TtsWrap();
  ~TtsWrap();

  static v8::Handle<v8::Value> CreateWaveform(const v8::Arguments& args);
  static v8::Handle<v8::Value> New(const v8::Arguments& args);
};

} // namespace

NODE_MODULE(tts, tts::Init)

#endif // TTS_TTS_WRAP_H_

