function FrontBase() {

}

FrontBase.prototype.listenAuthBoxHover=function () {
    var authBox = $('.auth-box');
    var userMoreBox = $('.user-more-box');
    authBox.hover(function () {
        userMoreBox.show()
    },function () {
        userMoreBox.hide()
    })
};


FrontBase.prototype.Run = function () {
  var self = this;
  self.listenAuthBoxHover();
};

$(function () {
   var fbase = new FrontBase();
   fbase.Run();
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


function Auth() {
    var  self =this;
    self.maskWrapper = $('.mask-wrapper')
}

Auth.prototype.run=function(){
    var self =this;
    self.listenShowhideEvent();
    self.listenSignInEvent();
    self.ListCaptchaClick();
    self.listenSmsCaptchaEvent();
    self.listenSignupEvent();
};

Auth.prototype.showEvent=function() {
    var self =this;
    self.maskWrapper.show();
};

Auth.prototype.hideEvent = function(){
  var self =this;
  self.maskWrapper.hide()
};


Auth.prototype.ListCaptchaClick=function(){
    var img =$('.img-captcha');
    img.click(function () {
        img.attr('src','/account/img_captcha/'+'?random'+Math.random())
    });
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

//短信验证码发送成功的事件
Auth.prototype.SmsSuccessEvent =function(){
    var self =this;
    var smsCaptcha= $('.sms-captcha-addon');
    messageBox.showSuccess("短信验证码发送成功");
    smsCaptcha.addClass('disabled');
    var count=60;
    smsCaptcha.unbind('click');
    var time =setInterval(function () {
        smsCaptcha.text(count+'s');
        count--;
        if(count<=0){
            clearInterval(time);
            smsCaptcha.removeClass('disabled');
            smsCaptcha.text('发送验证码');
            self.listenSmsCaptchaEvent();
        }
        },1000);
};


Auth.prototype.listenSignupEvent = function () {
    var signupGroup = $('.signup-group');
    var submitBtn = signupGroup.find('.submit-btn');
    submitBtn.click(function (event) {
        event.preventDefault();
        var telephoneInput = signupGroup.find("input[name='telephone']");
        var usernameInput = signupGroup.find("input[name='username']");
        var imgCaptchaInput = signupGroup.find("input[name='img_captcha']");
        var password1Input = signupGroup.find("input[name='password1']");
        var password2Input = signupGroup.find("input[name='password2']");
        var smsCaptchaInput = signupGroup.find("input[name='sms_captcha']");

        var telephone = telephoneInput.val();
        var username = usernameInput.val();
        var img_captcha = imgCaptchaInput.val();
        var password1 = password1Input.val();
        var password2 = password2Input.val();
        var sms_captcha = smsCaptchaInput.val();

        xfzajax.post({
            'url': '/account/register/',
            'data': {
                'telephone': telephone,
                'username': username,
                'img_captcha': img_captcha,
                'password1': password1,
                'password2': password2,
                'sms_captcha': sms_captcha
            },
            'success': function (result) {
                window.location.reload();
            }
        });
    });
};


//监听发送短信验证码的事件
Auth.prototype.listenSmsCaptchaEvent=function(){
    var self =this;
    var smsCaptcha= $('.sms-captcha-addon');
    var telePhoneInput = $(".signup-group input[name='telephone']");
    smsCaptcha.click(function () {
        var tele =telePhoneInput.val();
        if(!tele){
            messageBox.showInfo('请输入手机号码')
        }
        xfzajax.get({
                'url': '/account/sms_captcha/',
                'data':{
                    'telephone':tele
                } ,
                'success':function (result) {
                    if(result['code']==200){
                        self.SmsSuccessEvent();
                    }

                },
                'fail':function (error) {
                    console.log(error)
                }
            }
        )
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


$(function () {
    if(template){
        template.defaults.imports.timeSince = function (dateValue) {
            var date = new Date(dateValue);
            var datets = date.getTime(); // 得到的是毫秒的
            var nowts = (new Date()).getTime(); //得到的是当前时间的时间戳
            var timestamp = (nowts - datets)/1000; // 除以1000，得到的是秒
            if(timestamp < 60) {
                return '刚刚';
            }
            else if(timestamp >= 60 && timestamp < 60*60) {
                minutes = parseInt(timestamp / 60);
                return minutes+'分钟前';
            }
            else if(timestamp >= 60*60 && timestamp < 60*60*24) {
                hours = parseInt(timestamp / 60 / 60);
                return hours+'小时前';
            }
            else if(timestamp >= 60*60*24 && timestamp < 60*60*24*30) {
                days = parseInt(timestamp / 60 / 60 / 24);
                return days + '天前';
            }else{
                var year = date.getFullYear();
                var month = date.getMonth();
                var day = date.getDay();
                var hour = date.getHours();
                var minute = date.getMinutes();
                return year+'/'+month+'/'+day+" "+hour+":"+minute;
            }
        }
    }
});