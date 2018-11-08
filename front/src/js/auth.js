

//点击登陆按钮，弹出模态对话框
$(function () {
   $('#btn').click(function () {
       $('.mask-wrapper').show();
   }) ;

    $('.close-btn').click(function () {
       $('.mask-wrapper').hide();
    })
});


$(function () {
   $('.switch').click(function () {
        var scrollWrapper=$('.scroll-wrapper');
        var currentleft = parseInt(scrollWrapper.css('left'));
        if(currentleft<0)
        {
            scrollWrapper.animate({'left':'0'})
        }
        else
        {
            scrollWrapper.animate({'left':'-400px'})
        }
   })
});