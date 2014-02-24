KEY_CODE_ESCAPE = 27

Template.dinoRapping.created = ->
  SFX.final.tryPlay()

Template.dinoRapping.rendered = ->
  return if @alreadyRendered
  @alreadyRendered = true

  pop = Popcorn('#rap-audio')
  overlay = $('.overlay')

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

