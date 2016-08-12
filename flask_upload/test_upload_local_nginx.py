#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# upload demo

import os
import flask
from flask import request
from werkzeug import secure_filename

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'tmp'
app.config['MAX_CONTENT_LENGTH'] = 1<<1240  # max upload size < 16M

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'upload success'

@app.route('/', methods=['GET'])
def explore():
    ''' server upload '''
    return ''' 
<!doctype html>
<title>Upload new File</title>
<head>
<link rel="stylesheet" type="text/css" href="/static/css/webuploader.css">
<link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css">
<script type="text/javascript" src="/static/js/jquery-1.10.2.min.js"></script>
<script type="text/javascript" src="/static/js/bootstrap.min.js"></script>
<script type="text/javascript" src="/static/js/webuploader.min.js"></script>
</head>
<body>
<h1>Upload new File</h1>
<div id="uploader" class="wu-example">
    <!--用来存放文件信息-->
    <div id="thelist" class="uploader-list"></div>
    <div class="btns">
        <div id="pickerfile">选择文件</div>
        <button id="ctlBtn" class="btn btn-default">开始上传</button>
    </div>
</div>
<script>
$(function(){
var $list=$("#thelist");   //这几个初始化全局的百度文档上没说明，好蛋疼。  
var $btn =$("#ctlBtn");   //开始上传
var uploader = WebUploader.create({
    auto:true,

    swf: 'http://192.168.208.212/static/js/Upload.swf',
    // 文件接收服务端。
    server: 'http://192.168.208.212/upload',

    // 选择文件的按钮。可选。
    // 内部根据当前运行是创建，可能是input元素，也可能是flash.
    pick: '#pickerfile',

    // 不压缩image, 默认如果是jpeg，文件上传前会压缩一把再上传！
    resize: false
});

uploader.on( 'fileQueued', function( file ) {
    $list.append( '<div id="' + file.id + '" class="item">' +
        '<h4 class="info">' + file.name + '</h4>' +
        '<p class="state">等待上传...</p>' +
    '</div>' );
});

uploader.on( 'uploadProgress', function( file, percentage ) {
    var $li = $( '#'+file.id ),
        $percent = $li.find('.progress .progress-bar');

    // 避免重复创建
    if ( !$percent.length ) {
        $percent = $('<div class="progress progress-striped active">' +
          '<div class="progress-bar" role="progressbar" style="width: 0%">' +
          '</div>' + '<label id="l_p"></label>' +
        '</div>').appendTo( $li ).find('.progress-bar');
    }

    $("#l_p").html(Math.round(percentage * 100) + '%');
    $li.find('p.state').text('上传中');

    $percent.css( 'width', percentage * 100 + '%' );
});

uploader.on( 'uploadSuccess', function( file ) {
    $( '#'+file.id ).find('p.state').text('已上传');
});

uploader.on( 'uploadError', function( file ) {
    $( '#'+file.id ).find('p.state').text('上传出错');
});

uploader.on( 'uploadComplete', function( file ) {
    $( '#'+file.id ).find('.progress').fadeOut();
});

});
</script>
</body>

'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
