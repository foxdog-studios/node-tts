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
          base: 'build'
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
        dest: 'build/audio'

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
        dest: 'build/img'

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
        dest: 'build/js/lib/vendor'

      sass:
        expand: true
        cwd: 'src'
        src: 'sass/**/*.sass'
        dest: 'build'


    # =========================================================================
    # = SASS                                                                  =
    # =========================================================================

    sass:
      compile:
        files:
          'build/css/style.css': 'build/sass/style.sass'
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
        files: 'build/index.html'
      img:
        files: 'res/*.gif'
        tasks: 'copy:img'
      sass:
        files: 'src/sass/**/*.sass'
        tasks: 'buildSass'
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
    default: ['rebuild', 'continuous']
    rebuild: ['clean', 'build']

  for task in gruntContribTasks
    grunt.loadNpmTasks 'grunt-contrib-' + task

  for name, subtasks of tasks
    grunt.registerTask name, subtasks

