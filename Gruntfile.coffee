module.exports = (grunt) ->
  grunt.initConfig
    connect:
      server:
        options:
          base: 'build/'
          port: 8000
    copy:
      img:
        files: [
          expand: true
          flatten: true
          cwd: 'res'
          src: [
            'dino.gif'
            'fatdino.gif'
            'fatterdino.gif'
            'finaldino.gif'
            'meltingdino.gif'
          ]
          dest: 'build/'
        ]
      js_vendor:
        files: [
          expand: true
          flatten: true
          cwd: 'bower_components'
          src: [
            'jquery/jquery.js'
            'popcornjs/popcorn.js'
            'popcornjs/effects/applyclass/popcorn.applyclass.js'
            'popcornjs/plugins/footnote/popcorn.footnote.js'
          ]
          dest: 'build/'
        ]
    watch:
      files: [
        'build/index.html'
      ]
      tasks: ['copy']
      options:
        livereload: true

  npmTasks = [
    'grunt-contrib-connect'
    'grunt-contrib-copy'
    'grunt-contrib-watch'
  ]

  for task in npmTasks
    grunt.loadNpmTasks(task)
  grunt.registerTask('default', ['copy', 'connect', 'watch'])

