class AudioSample
  constructor: (@_ctx, uri) ->
    request = new XMLHttpRequest
    request.open 'GET', uri, true
    request.responseType = 'arraybuffer'
    request.onload = =>
      @_ctx.decodeAudioData request.response, (buffer) =>
        @_buffer = buffer
    request.send()

  tryPlay: ->
    return false unless @_buffer?
    @_source = @_ctx.createBufferSource()
    @_source.buffer = @_buffer
    @_source.connect @_ctx.destination
    @_source.start 0
    true

class Sfx
  constructor: ->
    ctx = new AudioContext
    create = (name) -> new AudioSample ctx, "/#{ name }.ogg"

    @baby     = create 'baby'
    @fat      = create 'teenager'
    @melting  = create 'fat'
    @teenager = create 'kid'

@SFX = new Sfx
