function NewsCategory() {

}

NewsCategory.prototype.Run=function () {
    var self =this;
    self.listAddCategoryBtnEvent();
    self.listenEditCategoryBtnEvent();
    self.listenDelCategoryBtnEvent();
};

//监听添加新闻分类按钮的事件
NewsCategory.prototype.listAddCategoryBtnEvent = function(){
      var addBtn = $('#add-btn');
    addBtn.click(function () {
        xfzalert.alertOneInput({
            'title': '添加新闻分类',
            'placeholder': '请输入新闻分类',
            'confirmCallback': function (inpuValue) {
                xfzajax.post({
                    'url': '/cms/add_news_category/',
                    'data': {
                        'name': inpuValue
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            console.log(result);
                            window.location.reload();
                        }else{
                            xfzalert.close();
                            window.messageBox.showError(result['message'])
                        }
                    }
                });
            }
        });
    });
};


//监听编辑新闻类别按钮事件
NewsCategory.prototype.listenEditCategoryBtnEvent = function(){
    var self =this;
    var editbtn =$('.edit-btn');
    editbtn.click(function () {
        var current = $(this);
        var tr = current.parent().parent();
        var pk = tr.attr('data-pk');
        var name = tr.attr('data-name');
        xfzalert.alertOneInput({
            'title': '修改分类名称',
            'placeholder': '请输入新的分类名称',
            'value':name,
            'confirmCallback': function (inputValue) {
                xfzajax.post({
                    'url':'/cms/edit_news_category/',
                    'data':{
                        'pk':pk,
                        'name':inputValue
                    },
                    'success':function (result) {
                        if(result['code'] === 200){
                            window.location.reload();
                        }else{
                            xfzalert.close();
                        }
                    }
                })
            }
        })
    });
};

//监听删除新闻类别的按钮事件
NewsCategory.prototype.listenDelCategoryBtnEvent = function(){
    var self =this;
    var delBtn=$('.del-btn')
    delBtn.click(function () {
        var current=$(this)
        var tr =current.parent().parent()
        var pk =tr.attr('data-pk')
        var name =tr.attr('data-name')
        xfzalert.alertConfirm({
            'title':'是否确认删除',
            'confirmCallback':function () {
                xfzajax.post({
                    'url':'/cms/del_news_category/',
                    'data':{
                        'pk':pk,
                        'name':name
                    },
                    'success':function (result) {
                        if(result['code']===200){
                            window.location.reload()
                        }else{
                            xfzalert.close();
                        }
                    }
                })
                
            }
        })
    })
};


$(function () {
    var newsCategory = new NewsCategory();
    newsCategory.Run()
});