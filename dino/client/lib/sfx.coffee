class AudioSample
  constructor: (ctx, uri, options) ->
    options = _.defaults (options or {}),
      loop: false

    @_autostart = false
    @_ctx = ctx
    @_loop = options.loop
    @_ready = false

    request = new XMLHttpRequest
    request.open 'GET', uri, true
    request.responseType = 'arraybuffer'

    callback = (buffer) => @_setBuffer buffer
    request.onload = ->
      ctx.decodeAudioData request.response, callback

    request.send()

  _setBuffer: (buffer) ->
    @_buffer = buffer
    @_ready = true
    @start() if @_autostart

  start: ->
    if @_ready
      @_source.stop if @_source?
      @_source = @_ctx.createBufferSource()
      @_source.buffer = @_buffer
      @_source.connect @_ctx.destination
      @_source.loop = @_loop
      @_source.start 0
      @_autostart = false
    else
      @_autostart = true

  stop: ->
    return unless @_source?
    @_source.stop()
    @_autostart = false
    delete @_source


class Sfx
  constructor: ->
    ctx = new AudioContext

    create = (name, options) ->
      new AudioSample ctx, "/#{ name }.ogg", options

    @baby     = create 'baby'
    @fat      = create 'teenager'
    @melting  = create 'fat', loop: true
    @teenager = create 'kid'
    @final    = create 'final_form'

@SFX = new Sfx

