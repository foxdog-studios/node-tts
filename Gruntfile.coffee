# =============================================================================
# = Setup                                                                     =
# =============================================================================

# Add Ruby to the path
process.env['PATH'] += ":#{process.env['HOME']}/.gem/ruby/2.0.0/bin"


# =============================================================================
# = Configuration                                                             =
# =============================================================================

module.exports = (grunt) ->

  grunt.initConfig

    # =========================================================================
    # = Clean                                                                 =
    # =========================================================================

    clean: ['build']


    # =========================================================================
    # = Connect                                                               =
    # =========================================================================

    connect:
      serve:
        options:
          base: 'build/website'
          port: 8000
          middleware: (connect, options) -> [
            require('connect-livereload')()
            connect.static options.base
          ]


    # =========================================================================
    # = Copy                                                                  =
    # =========================================================================

    copy:
      audio:
        expand: true
        cwd: 'res'
        src: [
          'baby.ogg'
          'fat.ogg'
          'final_form.ogg'
          'kid.ogg'
          'teenager.ogg'
        ]
        dest: 'build/website/audio'

      img:
        expand: true
        cwd: 'res'
        src: [
          'dino.gif'
          'fatdino.gif'
          'fatterdino.gif'
          'finaldino.gif'
          'meltingdino.gif'
        ]
        dest: 'build/website/img'

      jsVendor:
        expand: true
        flatten: true
        cwd: 'bower_components'
        src: [
          'jquery/jquery.js'
          'popcornjs/popcorn.js'
          'popcornjs/effects/applyclass/popcorn.applyclass.js'
          'popcornjs/plugins/footnote/popcorn.footnote.js'
        ]
        dest: 'build/website/js/lib/vendor'

      sass:
        expand: true
        cwd: 'src'
        src: '**/*.sass'
        dest: 'build/website'

      tts:
        expand: true
        cwd: 'src'
        src: 'tts/**'
        dest: 'build'


    # =========================================================================
    # = SASS                                                                  =
    # =========================================================================

    sass:
      compile:
        files:
          'build/website/css/style.css': 'build/website/sass/style.sass'
        options:
          sourcemap: true


    # =========================================================================
    # = Watch                                                                 =
    # =========================================================================

    watch:
      audio:
        files: 'res/**/*.ogg'
        tasks: 'copy:audio'
      html:
        files: 'build/website/index.html'
      img:
        files: 'res/*.gif'
        tasks: 'copy:img'
      sass:
        files: 'src/sass/**/*.sass'
        tasks: 'buildSass'
      tts:
        files: 'src/tts/**'
        tasks: 'copy:tts'
      options:
        livereload: true


  # ===========================================================================
  # = Tasks                                                                   =
  # ===========================================================================

  gruntContribTasks = [
    'clean'
    'connect'
    'copy'
    'sass'
    'watch'
  ]

  tasks =
    build: ['copy', 'sass']
    buildSass: ['copy:sass', 'sass']
    continuous: ['connect', 'watch']
    default: ['build', 'continuous']
    rebuild: ['clean', 'build']

  for task in gruntContribTasks
    grunt.loadNpmTasks 'grunt-contrib-' + task

  for name, subtasks of tasks
    grunt.registerTask name, subtasks

