Template.dinoGrowing.rendered = ->
  if getProgress() > 0
    @data.sound.start()

Template.dinoGrowing.destroyed = ->
  @data.sound.stop()

Template.dinoGrowing.helpers
  progressPercent: ->
    progress = getProgress()
    progress.toFixed 1

