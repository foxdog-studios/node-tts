Template.powerUp.helpers
  phoneNumberLines: ->
    [
      Meteor.settings.public.phoneNumberLine1
      Meteor.settings.public.phoneNumberLine2
      Meteor.settings.public.phoneNumberLine3
    ]

  imageSrc: ->
    'dino.gif'

  imageWidth: ->
    rap = Raps.findOne()
    return 0 unless rap?
    return rap.numWords if rap.numWords == 0
    numWords = 0
    Sms.find({}).forEach (sms) ->
      numWords += sms.message.split(' ').length
    (numWords / rap.numWords) * 100

