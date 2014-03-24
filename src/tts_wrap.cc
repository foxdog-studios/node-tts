#include <cstring>
#include <vector>

#include <node_buffer.h>

#include "tts_wrap.h"

using namespace v8;

namespace tts {

void Init(Handle<Object> exports) {
  TtsWrap::Init(exports);
}

Persistent<Function> TtsWrap::constructor;

TtsWrap::TtsWrap() : tts_() {
  tts_.TryOpen();
}

TtsWrap::~TtsWrap() {
  tts_.TryClose();
}

void TtsWrap::Init(Handle<Object> exports) {
  Local<FunctionTemplate> tpl = FunctionTemplate::New(New);
  tpl->SetClassName(String::NewSymbol("Tts"));
  tpl->InstanceTemplate()->SetInternalFieldCount(1);
  tpl->PrototypeTemplate()->Set(
      String::NewSymbol("createWaveform"),
      FunctionTemplate::New(CreateWaveform)->GetFunction());
  constructor = Persistent<Function>::New(tpl->GetFunction());
  exports->Set(String::NewSymbol("Tts"), constructor);
}

Handle<Value> TtsWrap::CreateWaveform(const Arguments& args) {
  HandleScope scope;

  // Create the waveform.
  TtsWrap* const tts_wrap = ObjectWrap::Unwrap<TtsWrap>(args.This());
  String::Utf8Value utf8_text(args[0]->ToString());
  std::string text(static_cast<char*>(*utf8_text));
  std::vector<char> waveform = tts_wrap->tts_.CreateWaveform(text);

  // Create a JavaScript buffer containing the waveform.
  node::Buffer* slow_buffer = node::Buffer::New(waveform.size());
  memcpy(node::Buffer::Data(slow_buffer), &waveform[0], waveform.size());
  Local<Object> global = Context::GetCurrent()->Global();
  Local<Function> buffer_constructor = Local<Function>::Cast(
      global->Get(String::New("Buffer")));
  Handle<Value> buffer_args[3] = {
    slow_buffer->handle_,
    v8::Integer::New(waveform.size()),
    v8::Integer::New(0)
  };
  Local<Object> buffer = buffer_constructor->NewInstance(3, buffer_args);
  return scope.Close(buffer);
}

Handle<Value> TtsWrap::New(const Arguments& args) {
  HandleScope scope;
  if (args.IsConstructCall()) {
    TtsWrap* const tts = new TtsWrap();
    tts->Wrap(args.This());
    return args.This();
  } else {
    const int argc = 0;
    Local<Value> argv[argc] = { };
    return scope.Close(constructor->NewInstance(argc, argv));
  }
}

} // namespace

