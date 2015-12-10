var gulp = require('gulp');
var source = require('vinyl-source-stream'); // Used to stream bundle for further handling etc.
var browserify = require('browserify');
var watchify = require('watchify');
var reactify = require('reactify'); 
var concat = require('gulp-concat');
var connect = require('gulp-connect');

gulp.task('browserify', function() {
    var bundler = browserify({
        entries: ['./src/js/main.js'],
        transform: [reactify],
        debug: true,
        cache: {}, packageCache: {}, fullPaths: true
    });
    var watcher  = watchify(bundler);

    return watcher
    .on('update', function () {
        var updateStart = Date.now();
        console.log('Updating!');
        watcher.bundle()
        .pipe(source('./src/js/main.js'))
        .pipe(gulp.dest('./dist/'));
        console.log('Updated!', (Date.now() - updateStart) + 'ms');
    })
    .bundle()
    .pipe(source('./src/js/main.js'))
    .pipe(gulp.dest('./dist/build/'));
});

gulp.task('css', function () {
    gulp.watch('./src/**/*.css', function () {
        return gulp.src('./src/**/*.css')
        .pipe(concat('app.css'))
        .pipe(gulp.dest('dist/'));
    });
});

gulp.task('webserver', function() {
    connect.server({
        root: [__dirname, 'dist'],
        livereload: true,
        port:8889
    });
});

gulp.task('default', ['browserify', 'css', 'webserver']);