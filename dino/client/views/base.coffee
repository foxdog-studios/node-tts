Template.tts.helpers
  currentWords: ->
    numWords = 0
    Sms.find({}).forEach (sms) ->
      numWords += sms.message.split(' ').length
    numWords

  rap: -> Raps.findOne()
  sms: -> Sms.find {}

