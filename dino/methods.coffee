Meteor.methods
  'addRap': (rap, lyrics) ->
    check rap, String
    id = Raps.findOne()._id
    Raps.update id,
      $set:
        lyrics: lyrics
        rap: rap
    return

  'addSms': (number, words) ->
    check number, String
    check words, [String]
    Sms.insert number: number, words: words
    return

  'reset': (numWords) ->
    check numWords, Match.Integer
    Sms.remove {}
    Raps.remove {}
    Raps.insert numWords: numWords
    return

