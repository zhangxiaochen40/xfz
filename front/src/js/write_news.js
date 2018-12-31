function News() {

}

News.prototype.run = function(){
    var self = this;
    // self.listenFileUpload();
    self.Ueditor();
    self.listenQiniuFileUpLoad();
    self.submitContent();

};

//提交新闻内容
News.prototype.submitContent=function() {
    var submitBtn=$('#submit-btn');
    var btn =$(this)
    var news_data = btn.attr('data-news-id');
    var url='';
    if(news_data){
        url='cms/edit_news/'
    }else{
        url='/cms/write_news/'
    }
    submitBtn.click(function (event) {
        event.preventDefault();
        var title =  $("input[name='title']").val();
        var category = $("select[name='category']").val();
        var desc = $("input[name='desc']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = window.ue.getContent();

        xfzajax.post({
            'url': url,
            'data': {
                'title': title,
                'category': category,
                'desc': desc,
                'thumbnail': thumbnail,
                'content': content,
            },
            'success': function (result) {
                if(result['code'] === 200){
                    xfzalert.alertSuccess('恭喜！新闻发表成功！',function () {
                        window.location.reload();
                    });
                }
            }
        });
    });
};


News.prototype.Ueditor= function(){
	window.UEDITOR_CONFIG.initialFrameHeight = 600;


    window.ue = UE.getEditor('editor',{
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/'
    });
};


//用七牛云山传文件
News.prototype.listenQiniuFileUpLoad=function(){
    var self = this;
    var uploadBtn=$('#thumbnail-btn');
    uploadBtn.change(function (event) {
        var file =this.files[0];
        xfzajax.get({
            'url':'/cms/token/',
            'success':function (result) {
                if(result['code']===200){
                    var token=result['data']['token'];
                    var key = (new Date()).getTime()+'.'+file.name.split('.')[1];
                    var putExtra={
                        fname:key,
                        params:{},
                        mimeType:['image/png','image/jpeg','image/gif','video/x-ms-wmv']
                    };
                    var config={
                        useCdnDomain: true,
                        retryCount: 6,
                        region: qiniu.region.z2
                    };
                    var observable = qiniu.upload(file,key,token,putExtra,config);
                     observable.subscribe({

                        'next': self.handleFileUploadProgress,
                        'error': self.handleFileUploadError,
                        'complete': self.handleFileUploadComplete
                    });
                }
            }
        })
    })
};


News.prototype.handleFileUploadProgress = function (response) {
    var total = response.total;
    var percent = total.percent;
    var percentText = percent+'%';
    // 24.0909，89.000....
    var progressGroup = $('#progress-group');
    progressGroup.show();
    var progressBar = $(".progress-bar");
    progressBar.css({"width":percentText});
    progressBar.text(percentText);
};

News.prototype.handleFileUploadError = function (error) {
    window.messageBox.showError(error.message);
    var progressGroup = $("#progress-group");
    progressGroup.hide();
    console.log(error.message);
};

News.prototype.handleFileUploadComplete = function (response) {
    console.log(response);
    var progressGroup = $("#progress-group");
    progressGroup.hide();

    var domain = 'http://pj5zy7xe1.bkt.clouddn.com/';
    var filename = response.key;
    var url = domain + filename;
    var thumbnailInput = $("input[name='thumbnail']");
    thumbnailInput.val(url);
};

//文件上传事件
News.prototype.listenFileUpload = function(){
    var uploadBtn=$('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file',file);
        xfzajax.post({
            'url':'/cms/upload_file/',
            'data':formData,
            'processData':false,
            'contentType':false,
            'success':function (result) {
                if(result['code']===200)
                {
                    var url = result['data']['url'];
                    var thumbnailInput = $('#thumbnail-form');
                    thumbnailInput.val(url);
                }
            }
        })
    })
};


$(function () {
   var news =new News();
    news.run();
});