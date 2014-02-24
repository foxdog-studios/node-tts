KEY_CODE_ESCAPE = 27

Template.dinoRapping.created = ->
  createAudioSample new AudioContext(), 'final_form.ogg', true

Template.dinoRapping.rendered = ->
  return if @alreadyRendered
  @alreadyRendered = true

  pop = Popcorn('#rap-audio')

  $(window).keyup (event) ->
    switch event.keyCode
      when KEY_CODE_ESCAPE
        pop.play()

Template.dinoRapping.helpers
  audioSrc: ->
    rap = Raps.findOne()
    return unless rap?.rap?
    rap.rap

