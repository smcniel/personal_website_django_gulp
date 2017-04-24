/*jslint node: true */
'use strict';

// Gulp plugins
var gulp                           = require('gulp'),
    del                            = require('del'),
    sass                           = require('gulp-sass'),
    CSSCompressor                  = require('gulp-csso'),
    browserSpecificPrefixGenerator = require('gulp-autoprefixer'),
    HTMLMinifier                   = require('gulp-htmlmin'),
    HTMLValidator                  = require('gulp-html'),
    JSConcatenator                 = require('gulp-concat'),
    JSLinter                       = require('gulp-jshint'),
    JSCompressor                   = require('gulp-uglify'),
    imageCompressor                = require('gulp-imagemin'),
    tempCache                      = require('gulp-cache'),
    browserSync                    = require('browser-sync'),
    // gulpif                         = require('gulp-if'),
    gutil                          = require('gulp-util'),
    reload                         = browserSync.reload,
    // spawn                          = require('child_process').spawn,

    // Folder name variables
    devSourceFolder  = './website/static/dev',
    devTargetFolder  = './website/static/build',
    // prodTargetFolder = 'prod',
    HTMLSourceFolder = './website/templates',
    JSFolder         = 'scripts',
    imagesFolder     = 'images',
    sassCSSFolder    = 'styles',

    // Filenames and paths
    JSTargetFilename = 'main.js',
    preConcatenatedJSFiles = devSourceFolder + '/' + JSFolder + '/*.js',
    HTMLFiles = [
        HTMLSourceFolder + '/*.html',
        HTMLSourceFolder + '/**/*.html'
    ],
    sassMainFile = devSourceFolder  + '/' + sassCSSFolder + '/main.scss',

    // Folder paths
    expendableStyles         = devTargetFolder + '/' + sassCSSFolder,
    expendableJS             = devTargetFolder + '/' + JSFolder,
    // expendableFolders        = [expendableStyles, expendableJS, prodTargetFolder],
    expendableFolders        = [expendableStyles, expendableJS],
    JSDevTargetFolder        = devTargetFolder  + '/' + JSFolder,
    // JSProdTargetFolder       = prodTargetFolder + '/' + JSFolder,
    cssDevDestinationFolder  = devTargetFolder  + '/' + sassCSSFolder;
    // cssDevDestinationFolder  = devTargetFolder  + '/static/' + sassCSSFolder + '/';
    // cssProdDestinationFolder = prodTargetFolder + '/' + sassCSSFolder + '/';



/**
 * COMPILE CSS FOR DEVELOPMENT WORK
 *
 * This task looks for a single Sass file (sassMainFile), compiles the CSS from it,
 * and writes the resulting file to the cssDevDestinationFolder. The final CSS file
 * will be formatted with 2-space indentations. Any floating-point calculations will
 * be carried out 10 places, and browser-specific prefixes will be added to support 2
 * browser versions behind all current browsers’ versions.
 */
gulp.task('compileCSSForDev', function () {
    return gulp.src(sassMainFile)
        .pipe(sass({
            outputStyle: 'expanded',
            precision: 10
        }).on('error', sass.logError))
        .pipe(browserSpecificPrefixGenerator({
            browsers: ['last 2 versions']
        }))
        .pipe(gulp.dest(cssDevDestinationFolder));
});

/**
 * COMPILE CSS FOR PRODUCTION
 *
 * This task looks for a single Sass file (sassMainFile), compiles the CSS from it,
 * and writes the resulting single CSS file to the cssProdDestinationFolder. Any
 * floating-point calculations will be carried out 10 places, and browser-specific
 * prefixes will be added to support 2 browser versions behind all current browsers’
 * versions. Lastly, the final CSS file is passed through two levels of compression:
 * “outputStyle” from Sass and compressCSS().
 */
// gulp.task('compileCSSForProd', function () {
//     return gulp.src(sassMainFile)
//         .pipe(sass({
//             outputStyle: 'compressed',
//             precision: 10
//         }).on('error', sass.logError))
//         .pipe(browserSpecificPrefixGenerator({
//             browsers: ['last 2 versions']
//         }))
//         .pipe(CSSCompressor())
//         .pipe(gulp.dest(cssProdDestinationFolder));
// });

/**
 * CONCATENATE JAVASCRIPT FILES
 *
 * This task concatenates all the files in the preConcatenatedJSFiles array, using
 * the JSConcatenator, then writes the result to the JSDevTargetFolder with the
 * filename value to the JSTargetFilename variable.
 */
gulp.task('concatenateJSFiles', function () {
    return gulp.src(preConcatenatedJSFiles)
        .pipe(JSConcatenator(JSTargetFilename))
        .pipe(gulp.dest(JSDevTargetFolder));
});

/**
 * CONCATENATE JAVASCRIPT FOR PRODUCTION
 *
 * This task compiles one or more JavaScript files into a single file whose name is
 * the value to the JSTargetFilename variable. The resulting file is compressed then
 * written to the JSProdTargetFolder.
 *
 * Note: This task does not contain the grid used during development.
 */
// gulp.task('concatenateJSForProd', ['concatenateJSFiles'], function () {
//     return gulp.src(JSDevTargetFolder + '/' + JSTargetFilename)
//         .pipe(JSCompressor())
//         .pipe(gulp.dest(JSProdTargetFolder));
// });

/**
 * LINT JAVASCRIPT
 *
 * This task lints JavaScript (JS) using the linter defined by JSLinter, the second
 * pipe in this task. (JSHint is the linter in this case.) In order to generate a
 * linting report, the multiple JS files in the preConcatenatedJSFiles are
 * compiled into a single, memory-cached file with a temporary name, then sent to the
 * linter for processing.
 *
 * Note: The temporary file is *not* written to a destination folder.
 */
gulp.task('lintJS', function () {
    return gulp.src(preConcatenatedJSFiles)
        .pipe(JSConcatenator(JSTargetFilename))
        .pipe(JSLinter())
        .pipe(JSLinter.reporter('jshint-stylish'))
        .pipe(JSLinter.reporter('fail'));
});

/**
 * COMPRESS THEN COPY IMAGES TO THE PRODUCTION FOLDER
 *
 * This task sources all the images in the devSourceFolder, compresses PNGs and JPGs,
 * then copies the final compressed images to the prodTargetFolder.
 */
// gulp.task('compressThenCopyImagesToProdFolder', function () {
//     return gulp.src(devSourceFolder + '/' + imagesFolder + '/**/*')
//         .pipe(tempCache(
//             imageCompressor({
//                 optimizationLevel: 3, // For PNG files. Accepts 0 – 7; 3 is default.
//                 progressive: true,    // For JPG files.
//                 multipass: false,     // For SVG files. Set to true for compression.
//                 interlaced: false     // For GIF files. Set to true for compression.
//             })
//         ))
//         .pipe(gulp.dest(prodTargetFolder + '/' + imagesFolder));
// });

/**
 * COPY UNPROCESSED ASSETS TO THE PRODUCTION FOLDER
 *
 * This task copies all unprocessed assets in the devSourceFolder to the
 * prodTargetFolder that aren’t images, JavaScript, or Sass/CSS. This is because
 * those files are processed by other tasks, then copied after processing:
 *
 * — Images are compressed then copied by the compressThenCopyImagesToProdFolder task
 * — JavaScript is concatenated and compressed by the concatenateJSForProd task
 * — Sass/CSS is concatenated and compressed by the compileCSSForProd task
 */
// gulp.task('copyUnprocessedAssetsToProdFolder', function () {
//     return gulp.src([
//         devSourceFolder + '/*.*',                           // Source all files,
//         devSourceFolder + '/**',                            // and all folders, but
//         '!' + devSourceFolder + '/' + imagesFolder,         // ignore images;
//         '!' + devSourceFolder + '/**/*.js',                 // ignore JS;
//         '!' + devSourceFolder + '/' + sassCSSFolder + '/**' // ignore Sass/CSS.
//     ], {dot: true}).pipe(gulp.dest(prodTargetFolder));
// });

/**
 * BUILD
 *
 * This task validates HTML, lints JavaScript, compiles any files that require
 * pre-processing, then copies the pre-processed and unprocessed files to the
 * prodTargetFolder.
 */
gulp.task('build',
    [
        'validateHTML',
        'compressHTML',
        'compileCSSForProd',
        'lintJS',
        'concatenateJSForProd',
        'compressThenCopyImagesToProdFolder',
        'copyUnprocessedAssetsToProdFolder'
    ]);

/**
 * DEVELOP
 *
 * This is the main development task and runs after running the server.
 * It watches for changes to the static and template files, concatenates and
 * lints JavaScript, compiles the dev SASS files to a single CSS file,
 * then copies the processed static files to the devTargetFolder where Django
 * looks for them. Also, the browser reloads after a change.
 */

gulp.task('develop', function () {
    browserSync.init({
        notify: false,
        proxy: "http://127.0.0.1:8000/"
    });
    gulp.watch(devSourceFolder + '/' + JSFolder + '/*.js',
        ['concatenateJSFiles', 'lintJS']).on(
        'change',
        reload
    );

    gulp.watch(devSourceFolder + '/' + imagesFolder + '/**/*').on(
        'change',
        reload
    );

    gulp.watch(HTMLSourceFolder + '/**/*.html').on(
        'change',
        reload
    );

    gulp.watch(devSourceFolder + '/' + sassCSSFolder + '/**/*.scss',
        ['compileCSSForDev']).on(
        'change',
        reload
    );
});
/**
 * CLEAN
 *
 * This tasks deletes the devTargetFolder files and prodTargetFolder directories,
 * both of which are expendable, since Gulp can re-build them at any moment.
 */
gulp.task('clean', function () {
    var fs = require('fs');

    for (var i = 0; i < expendableFolders.length; i++ ) {
        try {
            fs.accessSync(expendableFolders[i], fs.F_OK);
            process.stdout.write('\n\tThe ' + expendableFolders[i] +
                ' directory was found and will be deleted.\n');
            del(expendableFolders[i]);
        } catch (e) {
            process.stdout.write('\n\tThe ' + expendableFolders[i] +
                ' directory does NOT exist or is NOT accessible.\n');
        }
    }

    process.stdout.write('\n');
});

/**
 * DEFAULT
 *
 * This task does nothing. See the output message below.
 */
gulp.task('default', function() {
    return gutil.log('Gulp running.');
});

// gulp.task('default', ['serve']);

