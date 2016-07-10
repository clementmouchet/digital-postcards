module.exports = function (grunt) {
    grunt.initConfig({

        pkg: grunt.file.readJSON('package.json'),

        less: {
            css: {
                files: {
                    'build/css/main_compiled.css': [
                        'digitalpostcards/static/less/main.less'
                    ],
                    'build/css/postcard_compiled.css': [
                        'digitalpostcards/static/less/postcard.less'
                    ]
                }
            }
        },
        autoprefixer: {
            css: {
                options: {
                    browsers: [
                        'Android 2.3',
                        'Android >= 4',
                        'Chrome >= 20',
                        'Firefox >= 24',
                        'Explorer >= 8',
                        'iOS >= 6',
                        'Opera >= 12',
                        'Safari >= 6'
                    ]
                },
                files: {
                    'digitalpostcards/static/css/main.css': [
                        'build/css/main_compiled.css'
                    ],
                    'digitalpostcards/static/css/postcard.css': [
                        'build/css/postcard_compiled.css'
                    ]
                }
            }
        },
        cssmin: {
            options: {
                sourceMap: true
            },
            target: {
                files: {
                    'digitalpostcards/static/css/main.min.css': [
                        'digitalpostcards/static/css/main.css'
                    ],
                    'digitalpostcards/static/css/postcard.min.css': [
                        'digitalpostcards/static/css/postcard.css'
                    ]
                }
            }
        },
        watch: {
            less: {
                files: 'digitalpostcards/static/less/*.less',
                tasks: ['less', 'autoprefixer', 'cssmin']
            }
        }

    });

    grunt.loadNpmTasks('grunt-autoprefixer');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('default', [
        'less',
        'autoprefixer',
        'cssmin',
        'watch'
    ]);
    grunt.registerTask('build', [
        'less',
        'autoprefixer',
        'cssmin'
    ]);
};
