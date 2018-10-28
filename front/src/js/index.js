function Banner() {
    this.bannerGroup = $("#banner-group");
    this.index = 0;
    //轮波图中一个轮波图的宽度
    this.bannerWidth=798;
    //监听鼠标划过轮波图的事件
    this.listenBannerHover();
    this.leftArrow=$('.left-arrow');
    this.rightArrow=$('.right-arrow');
    this.bannerUl =$('#banner-ul');
    this.liList = this.bannerUl.children('li');
    //轮波图的个数
    this.bannerCount = this.liList.length;

}

Banner.prototype.run=function () {
    var self = this;
    this.ininBanner();
    this.loop();
    this.toggelArrow();
    this.listenArrowClick();
    self.initPageControl()
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
        if(self.index>=1)
        {
            self.index=0;
        }
        else {

            self.index++;
        }
        self.animate();
    },2000);
};


$(function () {
    var banner =new Banner();
    banner.run();

});