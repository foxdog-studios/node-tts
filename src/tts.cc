#include <cassert>
#include <cstdlib>
#include <vector>

#include <swift.h>

#include "tts.h"

namespace tts {

Tts::Tts() : engine_(NULL), port_(NULL) {
}

Tts::~Tts() {
}

bool Tts::IsOpen() {
  return engine_ != NULL && port_ != NULL;
}

bool Tts::TryOpen() {
  return TryOpenEngine() && TryOpenPort() && TrySetVoice();
}

bool Tts::TryClose() {
  return TryClosePort() && TryCloseEngine();
}

std::vector<char> Tts::CreateWaveform(const std::string& text) {
  assert(IsOpen());
  waveform_.clear();
  swift_port_speak_text(port_, text.c_str(), 0, NULL, NULL, NULL);
  return std::vector<char>(waveform_);
}

bool Tts::TryLoadLexicon(const std::string& file) {
  assert(IsOpen());
  swift_voice* const voice = swift_port_get_current_voice(port_);
  if (voice == NULL) {
    return false;
  }
  return IsSuccess(swift_voice_load_lexicon(voice, file.c_str()));
}

bool Tts::TryOpenEngine() {
  engine_ = swift_engine_open(NULL);
  return engine_ != NULL;
}

bool Tts::TryCloseEngine() {
  const bool closed = IsSuccess(swift_engine_close(engine_));
  if (closed) {
    engine_ = NULL;
  }
  return closed;
}

bool Tts::TryOpenPort() {
  assert(!IsOpen());
  port_ = swift_port_open(engine_, NULL);
  bool opened = port_ != NULL;
  if (opened) {
    swift_port_set_callback(
        port_,
        &PortCallback,
        SWIFT_EVENT_AUDIO,
        &waveform_);
  }
  return opened;
}

bool Tts::TryClosePort() {
  const bool closed = IsSuccess(swift_port_close(port_));
  if (closed) {
    port_ = NULL;
  }
  return closed;
}

bool Tts::TrySetVoice() {
  return swift_port_set_voice_by_name(port_, "Amy") != NULL;
}

bool Tts::IsSuccess(const swift_result_t& result) {
  return result == SWIFT_SUCCESS;
}

swift_result_t PortCallback(swift_event* const event, swift_event_t const type,
                            void* const data) {
  // Retrieve the audio data.
  void* buf;
  int len;
  swift_result_t const result = swift_event_get_audio(event, &buf, &len);

  // Append the audio data to the output vector.
  if (!SWIFT_FAILED(result)) {
    char* const in = static_cast<char* const>(buf);
    std::vector<char>* const out = static_cast<std::vector<char>* const>(data);
    out->insert(out->end(), in, in + len);
  }

  return result;
}

} // namespace
