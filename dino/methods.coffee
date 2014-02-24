Meteor.methods
  'addRap': (rap) ->
    check rap, String
    id = Raps.findOne()._id
    Raps.update id, $set: rap: rap
    return

  'addSms': (number, message) ->
    check number, String
    check message, String
    Sms.insert number: number, message: message
    return

  'reset': (numWords) ->
    check numWords, Match.Integer
    Sms.remove {}
    Raps.remove {}
    Raps.insert numWords: numWords
    return

