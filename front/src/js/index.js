function Banner() {
    this.bannerGroup = $("#banner-group");
    this.index = 0;
    //轮波图中一个轮波图的宽度
    this.bannerWidth=798;

    this.leftArrow=$('.left-arrow');
    this.rightArrow=$('.right-arrow');
    this.bannerUl =$('#banner-ul');
    this.pageControl = $('.page-control');
    this.liList = this.bannerUl.children('li');
    //轮波图的个数
    this.bannerCount = this.liList.length;

}

Banner.prototype.run=function () {
    var self = this;
    this.ininBanner();
    this.loop();
    this.toggelArrow();
    //监听鼠标划过轮波图的事件
    this.listenBannerHover();
    this.listenArrowClick();

    self.initPageControl();
    this.listenPageControl();
};

//监听轮波图的小点点 的点击事件
Banner.prototype.listenPageControl = function(){
    var self =this;
    self.pageControl.children("li").each(function (index,obj) {
        $(obj).click(function () {
            self.index=index;

            self.animate();

        });
    });
};


Banner.prototype.listenBannerHover = function(){
    var self = this;
    this.bannerGroup.hover(function () {
        //第一个函数是把鼠标移动到轮波图上执行的函数
        clearInterval(self.timer);
        self.toggelArrow();
    },function () {
        //第二个方法是把鼠标从轮波图上移走时执行的函数
        self.loop();
        self.toggelArrow();
    })
};

//监听箭头的点击事件
Banner.prototype.listenArrowClick = function(){
    var self = this;
    //左边的箭头
    this.leftArrow.click(function () {
        if(self.index===0)
        {
            self.index = self.bannerCount-1;
        }
        else
        {
            self.index--;
        }
        self.animate();
    });
    //右边的箭头
    this.rightArrow.click(function () {
        if(self.index === self.bannerCount-1)
        {
            self.index=0;
        }
        else
        {
            self.index++;
        }
        // self.bannerUl.animate({'left':-798*self.index},500);
        self.animate();
    })
};

//初始化轮波图的小点点
Banner.prototype.initPageControl =function() {
    var self = this;
    var pageControl = $(".page-control");
    for (var i =0; i<self.bannerCount; i++) {
        var circle = $("<li></li>");
        pageControl.append(circle);
        if(i===0) {
             circle.addClass('active');
        }
    }
    pageControl.css({"width":self.bannerCount*12+8*2+16*(self.bannerCount-1)})
};

//设置轮波图的总共的宽度
Banner.prototype.ininBanner = function(){
    var self =this;
    this.bannerUl.css({"width":self.bannerWidth*self.bannerCount})
};


//封装一个轮波图移动的方法
Banner.prototype.animate = function(){
    var self =this;
    self.bannerUl.animate({'left':-798*self.index},500);
    self.pageControl.children('li').eq(self.index).addClass('active').siblings().removeClass('active')
};

//箭头的显示或隐藏
Banner.prototype.toggelArrow = function(){
    var self =this;
    self.leftArrow.toggle();
    self.rightArrow.toggle();

};

Banner.prototype.loop = function(){
    var bannerUl = $(".banner-ul");
    var index=0;
    var self = this;
    // bannerUl.animate({"left" : -798},500);
    this.timer = setInterval(function () {
        if(self.index>=self.bannerCount-1)
        {
            self.index=0;
        }
        else {

            self.index++;
        }
        self.animate();
    },2000);
};


function Index(){
   var self =this;
   self.page=2;
   self.category_id = 0;
   self.loadBtn = $("#load-more-btn");

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

Index.prototype.run =function(){
    var self =this;
    self.LoadMore();
    self.listenCategorySwitchEvent();
};

//加载更多按钮事件
Index.prototype.LoadMore=function(){
    var self =this;
    var loadBtn=$('#load-more-btn');
    loadBtn.click(function () {
        xfzajax.get({
            'url':'/news/list/',
            'data':{
                'p':self.page,
                'category_id':self.category_id
            },
            'success':function (result) {
                if(result['code']===200){
                    var newses = result['data'];
                    if(newses.length>0) {
                        var tpl = template('news-item', {'newses': newses});
                        var ul = $('.list-inner-group');
                        ul.append(tpl);
                        console.log(newses);
                        self.page += 1;
                    }else{
                        loadBtn.hide()
                    }
                }
            }
        })
    });
};

//监听新闻类别点击事件
Index.prototype.listenCategorySwitchEvent=function(){
        var self =this;
        var tagGroup=$('.list-tab');
        tagGroup.children().click(function () {
            var page = 1;
            var li = $(this);
             var category_id = li.attr("data-category")
            xfzajax.get({
                'url':'/news/list/',
                'data':{
                    'category_id':category_id,
                    'p':page
                },
                'success':function (result) {
                    if(result['code']===200){
                        var newses = result['data'];
                        var tpl = template('news-item', {'newses': newses});
                        var ul = $('.list-inner-group');
                        ul.empty()
                        ul.append(tpl);
                        self.page = 2;
                        self.category_id = category_id;
                        li.addClass('active').siblings().removeClass('active');
                        self.loadBtn.show()
                    }
                }

            })
        })

};


$(function () {
    var banner =new Banner();
    banner.run();
    var index =new Index();
    index.run();

});