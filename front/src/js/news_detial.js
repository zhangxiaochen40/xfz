function NewsList() {

}


NewsList.prototype.run=function () {
    var self =this;
    self.listenSubmitBtn();
};


NewsList.prototype.listenSubmitBtn=function(){
    var self =this;
    var submitBtn = $('.submit-btn');
    var textarea = $("textarea[name='comment-textarea']")
    submitBtn.click(function () {
        var content = textarea.val();
        var news_id = submitBtn.attr('data-news-id');

        xfzajax.post({
            'url':'/news/comment',
            'data':{
                'content':content,
                'news_id':news_id,
            },
            'success':function (result) {
                if(result['code']===200){
                    var comment =result['data'];
                    var tpl = template('comment-item',{'comment':comment})
                    var commentlist= $('.comment-list');
                    commentlist.prepend(tpl);
                    window.messageBox.showSuccess('评论发表成功')
                    textarea.val("")
                }else{
                    window.messageBox.showError(result['message'])
                }
            }
        })
    })
};



$(function () {
    var news_list = new NewsList();
    news_list.run()
});