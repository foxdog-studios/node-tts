audioCtx = new AudioContext

DINO_SCHEMA =
  baby:
    sound: createAudioSample audioCtx, '/baby.ogg'
    image: '/dino.gif'
  fat:
    sound: createAudioSample audioCtx, '/teenager.ogg'
    image: '/fatterdino.gif'
  teenager:
    sound: createAudioSample audioCtx, '/kid.ogg'
    image: '/teenagedino.gif'
  melting:
    sound: createAudioSample audioCtx, '/fat.ogg'
    image: '/meltingdino.gif'
    loop: true

Template.dinoPen.helpers
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
  return 0 if not rap? or rap?.numWords == 0
  console.log getCurrentWordCount()
  (getCurrentWordCount() / rap.numWords) * 100

getCurrentWordCount = ->
  count = 0
  Sms.find({}).forEach (sms) ->
    count += sms.message.split(' ').length
  count

