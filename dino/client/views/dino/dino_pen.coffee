audioCtx = new AudioContext

DINO_SCHEMA =
  baby:
    sound: SFX.baby
    image: '/dino.gif'
  fat:
    sound: SFX.fat
    image: '/fatterdino.gif'
  teenager:
    sound: SFX.teenager
    image: '/teenagedino.gif'

Template.dinoPen.helpers
  hasEnoughWords: -> getProgress() >= 100

  hasRap: -> Raps.findOne()?.rap?

  dino: ->
    progress = getProgress()
    name = switch
      when progress <  33 then 'baby'
      when progress <  66 then 'teenager'
      when progress < 100 then 'fat'
      else 'melting'
    DINO_SCHEMA[name]

getProgress = ->
  rap = Raps.findOne()
  if not rap? or rap?.numWords == 0
    return 0
  (getCurrentWordCount() / rap.numWords) * 100

getCurrentWordCount = ->
  count = 0
  Sms.find({}).forEach (sms) ->
    count += sms.message.split(' ').length
  count

