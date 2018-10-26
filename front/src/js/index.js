function Banner() {

}

Banner.prototype.run=function () {
    var bannerUl = $("#banner-ul");
    var index=0;
    // bannerUl.animate({"left" : -798},500);
    setInterval(function () {
        if(index>=1)
        {
            index=0;
        }
        else {

            index++;
        }
        bannerUl.animate({"left" : -798*index},500);
    },2000);
};

$(function () {
    var banner =new Banner();
    banner.run()
    
});