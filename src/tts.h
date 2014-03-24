#ifndef TTS_TTS_H_
#define TTS_TTS_H_

#include <string>
#include <vector>

#include <swift.h>

namespace tts {

class Tts {
 public:
  Tts();
  ~Tts();

  bool IsOpen();
  bool TryOpen();
  bool TryClose();

  std::vector<char> CreateWaveform(const std::string& text);

 private:
  swift_engine* engine_;
  swift_port* port_;
  std::vector<char> waveform_;

  bool TryOpenEngine();
  bool TryCloseEngine();

  bool TryOpenPort();
  bool TryClosePort();

  static bool IsSuccess(const swift_result_t& result);
};

swift_result_t PortCallback(swift_event* event, swift_event_t type, void* data);

} // namespace

#endif // TTS_TTS_H_

