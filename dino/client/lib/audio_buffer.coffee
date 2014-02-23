loadAudio = (ctx, url, callback) ->
  request = new XMLHttpRequest
  request.open 'GET', url, true
  request.responseType = 'arraybuffer'
  request.onload = () ->
    ctx.decodeAudioData request.response, callback
  request.send()


class @AudioBuffer
  constructor: (@_ctx, name, options) ->
    @autoplay = options?.autoplay or false
    @loop = options?.loop or false
    @_loadAudio(name)

  _loadAudio: (name) ->
    loadAudio @_ctx, "/#{ name }", (buffer) =>
      console.log 'Loaded', name
      @buffer = buffer
      @tryPlay() if @autoplay

  tryPlay: ->
    return unless @buffer?
    @source = @_ctx.createBufferSource()
    @source.loop = @loop
    @source.buffer = @buffer
    @source.connect @_ctx.destination
    @source.start 0

