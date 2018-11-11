

// //点击登陆按钮，弹出模态对话框
// $(function () {
//    $('#btn').click(function () {
//        $('.mask-wrapper').show();
//    }) ;
//
//     $('.close-btn').click(function () {
//        $('.mask-wrapper').hide();
//     })
// });
//

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


function Auth() {
    var  self =this;
    self.maskWrapper = $('.mask-wrapper')
}

Auth.prototype.run=function(){
    var self =this;
    self.listenShowhideEvent();
};

Auth.prototype.showEvent=function() {
    var self =this;
    self.maskWrapper.show();
};

Auth.prototype.hideEvent = function(){
  var self =this;
  self.maskWrapper.hide()
};


Auth.prototype.listenShowhideEvent = function(){
    var self =this;
    var signinBtn=$('.signin-btn');
    var signupBtn=$('.signup-btn');
    var closeBtn=$('.close-btn');
    var scrollWrapper = $('.scroll-wrapper');
    signinBtn.click(function () {
        self.showEvent();
        scrollWrapper.css({'left':0});
    });

    signupBtn.click(function () {
        self.showEvent();
        scrollWrapper.css({'left':-400})
    });

    closeBtn.click(function () {
       self.hideEvent();
    });

};


$(function () {
   var auth = new Auth();
   auth.run();
});