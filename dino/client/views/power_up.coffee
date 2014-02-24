getNumberOfWordsSoFar = ->
  numWords = 0
  Sms.find({}).forEach (sms) ->
    numWords += sms.message.split(' ').length
  numWords

getProgressPercentage = ->
  rap = Raps.findOne()
  return 0 unless rap?
  return rap.numWords if rap.numWords == 0
  numWords = getNumberOfWordsSoFar()
  progressPercentage = (numWords / rap.numWords) * 100
  if progressPercentage > 100
    progressPercentage = 100
  progressPercentage

DINO_SCHEMA =
  baby:
    sound: 'baby.ogg'
    image: 'dino.gif'
  fat:
    sound: 'teenager.ogg'
    image: 'fatterdino.gif'
  teenager:
    sound: 'kid.ogg'
    image: 'teenagedino.gif'
  melting:
    sound: 'fat.ogg'
    image: 'meltingdino.gif'
    loop: true

getCurrentDino = ->
  progressPercentage = getProgressPercentage()
  dinoName = switch
    when progressPercentage >= 100 then 'melting'
    when progressPercentage >= 66 then 'fat'
    when progressPercentage >= 33 then 'teenager'
    else 'baby'
  return DINO_SCHEMA[dinoName]


Template.powerUp.rendered = ->
  return if @alreadyRendered
  @alreadyRendered = true
  audioContext = new AudioContext()
  for dinoName, dino of DINO_SCHEMA
    dino.buffer = new AudioBuffer(audioContext, dino.sound)
  Deps.autorun ->
    smsCursor = Sms.find({})
    smsCursor.observe
      added: (document) ->
        dino = getCurrentDino()
        dino.buffer.tryPlay()


Template.powerUp.helpers
  phoneNumberLines: ->
    [
      Meteor.settings.public.phoneNumberLine1
      Meteor.settings.public.phoneNumberLine2
      Meteor.settings.public.phoneNumberLine3
    ]

  imageSrc: ->
    dino = getCurrentDino()
    dino.image

  imageWidth: ->
    getProgressPercentage()

  canTextIn: ->
    getProgressPercentage() < 100

