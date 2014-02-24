Meteor.methods
  'addSms': (number, message) ->
    if _.isString(number) and _.isString message
      Sms.insert
        number: number
        message: message
    return

  'addRap': (rap) ->
    id = Raps.findOne()._id
    Raps.update id, $set: rap: rap
    return

  'reset': (numWords) ->
    if _.isNumber numWords
      Sms.remove {}
      Raps.remove {}
      Raps.insert
        numWords: numWords
    return

