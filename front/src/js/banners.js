function Banners() {

}


Banners.prototype.LoadData = function(){
    var self =this;
    xfzajax.get({
        'url':'/cms/banner_list/',
        'success':function (result) {
            if(result['code']===200){
               var banners = result['data'];
                for (var i=0;i<banners.length;i++){
                    var banner = banners[i];
                    var tpl = template('banner-item',{'banner':banner});
                    var bannerGroup=$('.banner-list-group');
                    bannerGroup.append(tpl);

                    var bannerItem = bannerGroup.find('.banner-item:last');

                    self.addImageSelectEvent(bannerItem);
                    self.addRemoveBtn(bannerItem);
                    self.saveBannerEvent(bannerItem);
                }
            }else
            {
                console.log('cuowu')
            }
        }
    })
};


Banners.prototype.listenBannersAddBtn =function(){
    var self = this;
    var bannerBtn =$('#banner-add-btn');
    bannerBtn.click(function () {
        var bannerlistGroup = $('.banner-list-group');
        var bannerItems = bannerlistGroup.children().length;
        if (bannerItems>=6){
            window.messageBox.showError("最多不能超过6张轮波图");
            return;
        }
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
    var bannerId = bannerItem.attr('data-banner-id');
    var prioritySpan = bannerItem.find('span[class="priority"]');
    var url='';
    if(bannerId){
        url='/cms/edit_banner/'
    }else{
        url='/cms/add_banner/'
    }

    saveBtn.click(function () {
        var img_url = imageTag.attr('src');
        var priority = priorityTag.val();
        var link_to = link_toTag.val();
        xfzajax.post({
            'url':url,
            'data':{
                'img_url':img_url,
                'priority':priority,
                'link_to':link_to,
                'pk': bannerId,
            },
            'success':function (result) {
                    if(result['code']===200){
                        if(bannerId){
                            window.messageBox.showSuccess('轮播图修改完成！')
                        }else {
                            bannerId = result['data']['banner_id'];
                            bannerItem.attr('data-banner-id', bannerId);
                            window.messageBox.showSuccess('轮播图添加完成！');
                        }
                        prioritySpan.text("优先级："+priority);
                    }
            }
        })
    })
};


Banners.prototype.addImageSelectEvent = function (bannerItem) {
    var image = bannerItem.find('.thumbnail');
    var imageInput = bannerItem.find('.image-input');
    // 图片是不能够打开文件选择框的，只能通过input[type='file']
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
                    image.attr('src',url);
                }
            }
        });
    });
};


Banners.prototype.addRemoveBtn = function(bannerItem){
    var removeBtn = bannerItem.find('.btn-close');

    removeBtn.click(function () {
        var bannerId = bannerItem.attr('data-banner-id');
        if(bannerId)
        {
            xfzalert.alertConfirm({
                'text':'确定要删除吗',
                'confirmCallback':function () {
                    xfzajax.post({
                        'url':'/cms/delete_banner/',
                        'data':{
                            'banner_id':bannerId
                        },
                        'success':function (result) {
                            if(result['code']===200){
                                bannerItem.remove();
                                window.messageBox.showSuccess('轮播图删除成功')
                            }
                        }
                    })
                }
            })
        }
        else
        {
            bannerItem.remove()
        }
        
    })
};

Banners.prototype.Run =function () {
    var self =this;
    self.listenBannersAddBtn();
    self.LoadData();
};

$(function () {
    var banners =new Banners();
    banners.Run()
});