var gulp = require("gulp");
var cssnano = require("gulp-cssnano");
var rename = require("gulp-rename");
var uglify = require("gulp-uglify");
var concat = require("gulp-concat");
var cache = require('gulp-cache');
var imagemin = require('gulp-imagemin');
var bs = require('browser-sync').create();


var path = {
    'css' : './src/css/',
    'js' : './src/js/',
    'images' : './src/images/',
    'css_dist' : './dist/css',
    'js_dist' : './dist/js',
    'images_dist' : './dist/images/'
};


//定义一个css任务
gulp.task('css',function () {
    gulp.src(path.css+'*.css')
        .pipe(cssnano())
        .pipe(rename({'suffix':'.min'}))
        .pipe(gulp.dest(path.css_dist))
        .pipe(bs.stream)
});

//定义一个js任务
gulp.task('js',function () {
    gulp.src(path.js+'*.js')
        .pipe(uglify())
        .pipe(gulp.dest(path.js_dist))
        .pipe(bs.stream)
});

//定义一个图片处理的任务
gulp.task('images',function () {
    gulp.src(path.images+'*.*')
        .pipe(cache(imagemin()))
        .pipe(gulp.dest(path.images_dist))
});

//定义一个监听任务
gulp.task('watch',function () {
    gulp.watch(path.css+'*.css',['css']);
    gulp.watch(path.js+'*.js',['js']);
    gulp.watch(path.images+'*.images',['images']);
});

//初始化browser-sync的任务
gulp.task('bs',function () {
   bs.init({
       'server':{
           'baseDir':'./'
       }
   });
});

//创建一个默认的任务
gulp.task('default',['bs','watch']);