function Banners() {

}

Banners.prototype.listenBannersAddBtn =function(){
    var self = this;
    var bannerBtn =$('#banner-add-btn');
    bannerBtn.click(function () {
        var tpl =template('banner-item');
        var bannerGroup=$('.banner-list-group');
        bannerGroup.prepend(tpl);

        var bannerItem = bannerGroup.find('.banner-item:first');

        self.addImageSelectEvent(bannerItem);
        self.addRemoveBtn(bannerItem);
        self.saveBannerEvent(bannerItem);
    })
};


Banners.prototype.saveBannerEvent = function(bannerItem){
    var saveBtn = bannerItem.find('.btn-save');
    var priorityTag = bannerItem.find("input[name='priority']");
    var link_toTag = bannerItem.find(("input[name='link_to']"));
    var imageTag = bannerItem.find(".thumbnail");

    saveBtn.click(function () {
        var img_url = imageTag.attr('src');
        var priority = priorityTag.val();
        var link_to = link_toTag.val();
        xfzajax.post({
            'url':'/cms/add_banner/',
            'data':{
                'img_url':img_url,
                'priority':priority,
                'link_to':link_to
            },
            'success':function (result) {
                if(result['code']===200){
                    console.log('1111');
                    bannerId = result['data']['banner_id'];
                        bannerItem.attr('data-banner-id',bannerId);
                        window.messageBox.showSuccess('轮播图添加完成！');
                }
            }
        })
    })
};


Banners.prototype.addImageSelectEvent = function (bannerItem) {
    var image = bannerItem.find('.thumbnail');
    var imageInput = bannerItem.find('.image-input');
    // 图片是不能够打开文件选择框的，只能通过input[type='file']
    console.log('123123123');
    image.click(function () {
        imageInput.click();
    });

    imageInput.change(function () {
        var file = this.files[0];
        var formData = new FormData();
        formData.append("file",file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if(result['code'] === 200){
                    var url = result['data']['url'];
                    console.log(url)
                    image.attr('src',url);
                }
            }
        });
    });
};


Banners.prototype.addRemoveBtn = function(bannerItem){
    var removeBtn = bannerItem.find('.btn-close');
    removeBtn.click(function () {
        bannerItem.remove()
    })
};

Banners.prototype.Run =function () {
    var self =this;
    self.listenBannersAddBtn();
};

$(function () {
    var banners =new Banners();
    banners.Run()
});