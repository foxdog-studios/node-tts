KEY_CODE_ESCAPE = 27

CHUNK_SIZE = 3

Template.dinoRapping.created = ->
  SFX.final.tryPlay()

Template.dinoRapping.rendered = ->
  return if @alreadyRendered
  @alreadyRendered = true

  pop = Popcorn('#rap-audio')
  overlay = $('.overlay')

  Deps.autorun (computation) ->
    rap = Raps.findOne()
    return unless rap?.lyrics?
    lyrics = rap.lyrics
    chunks = for i in [0...lyrics.length] by CHUNK_SIZE
      lyrics[i...i+CHUNK_SIZE]
    for chunk, i in chunks
      start = chunk[0]
      startTime = start[1][1]
      if i < chunks.length - 1
        end = chunks[i+1][0]
        endTime = end[1][1]
      else
        # This is the last lyric, select it forever!
        endTime = null
      for lyric, i in chunk
        if i < chunk.length - 1
          lyricEndTime = chunk[i+1][1][1]
        else
          lyricEndTime = endTime
        target = "w#{i+1}"
        pop.footnote
          start: startTime
          end: endTime
          text: lyric[0]
          target: target
        pop.footnote
          start: lyric[1][1]
          end: lyricEndTime
          target: target
          text: ''
          effect: 'applyclass'
          applyclass: 'selected'


  $(window).keyup (event) ->
    switch event.keyCode
      when KEY_CODE_ESCAPE
        pop.play()
        overlay.toggle()

Template.dinoRapping.helpers
  audioSrc: ->
    rap = Raps.findOne()
    return unless rap?.rap?
    rap.rap

