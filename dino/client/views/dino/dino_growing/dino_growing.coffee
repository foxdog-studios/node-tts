Template.dinoGrowing.rendered = ->
  @data.sound.tryPlay()

Template.dinoGrowing.helpers
  progressPercent: ->
    progress = getProgress()
    progress.toFixed(1)

