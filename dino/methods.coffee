Meteor.methods
  'addSms': (number, message) ->
    if _.isString(number) and _.isString message
      Sms.insert
        number: number
        message: message

  'reset': (numWords) ->
    if _.isNumber numWords
      Sms.remove {}
      Raps.remove {}
      Raps.insert
        numWords: numWords

