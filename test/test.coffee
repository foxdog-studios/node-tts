@Utterances = new Meteor.Collection 'utterances'

insertUtterance = (text, options, callback) ->
  if _.isFunction options
    callback = options
    options = undefined
  options = {} unless options?

  check text, String
  check options, Match.Optional
    pitch: Match.Optional Match.Integer
    range: Match.Optional String

  pitch = options.pitch
  range = options.range

  # TODO: Replace with proper XML renderer.
  parts = ["<prosody"]
  parts.push " pitch=\"#{ pitch }\"" if pitch?
  parts.push " range=\"#{ range }\"" if range?
  parts.push ">#{ text }</prosody>"
  fields = ssml: parts.join ''

  Utterances.insert fields, callback

Meteor.methods
  setAudio: (id, audio) ->
    check id, String
    check audio, String
    numUpdated = Utterances.update id,
      $set:
        audio: audio
    numUpdated == 1

if Meteor.isServer
  Utterances.allow insert: -> true

  Meteor.publish 'ttsQueue', ->
    Utterances.find
      audio:
        $exists: false
    ,
      fields:
        ssml: 1

  Meteor.publish 'renderedUtterances', ->
    Utterances.find
      audio:
        $exists: true

  Meteor.startup ->
    Utterances.remove {}
    insertUtterance 'Hello, this is some text.',
      pitch: 300
      range: 'x-low'

if Meteor.isClient
  Meteor.subscribe 'renderedUtterances'

