

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
    self.listenSignInEvent();
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

Auth.prototype.listenSignInEvent=function(){
    var self =this;
    var signingroup = $('.signin-group');
    var telephone = signingroup.find("input[name='telephone']");
    var password = signingroup.find("input[name='password']");
    var remember = signingroup.find("input[name='remember']");

    var submitBtn= signingroup.find(".submit-btn");

    submitBtn.click(function () {
        var tel = telephone.val();
        var pwd =password.val();
        var rem = remember.prop('checked');

            xfzajax.post({
            'url': '/account/login/',
            'data': {
                'telephone': tel,
                'password': pwd,
                'remember': rem?1:0,
            },
            'success': function (result) {
                 if(result['code'] == 200){
                    self.hideEvent();
                    window.location.reload();
                 }else{
                     var messageObject = result['message'];
                     if(typeof messageObject == 'string' || messageObject.constructor == String){
                        window.messageBox.show(messageObject);
                     }else{
                        // {"password":['密码最大长度不能超过20为！','xxx'],"telephone":['xx','x']}
                        for(var key in messageObject){
                            var messages = messageObject[key];
                            var message = messages[0];
                            window.messageBox.show(message);
                        }
                     }

                 }
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    })
};


$(function () {
   var auth = new Auth();
   auth.run();
});