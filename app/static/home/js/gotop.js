$(document).ready(function () {
    var windowHeight = $(window).height();
// console.log(windowHeight);//785
    $(window).scroll(function () {
        var height_from_top = $(window).scrollTop();//var top_height = $(document).scrollTop();
        // console.log(height_from_top);
        if (height_from_top >= windowHeight) {
            $('#go_top').css("display", "block");
        } else {
            $('#go_top').css("display", "none");
        }
    });
    $('#go_top').click(function () {
        timer = setInterval(function () {
            var height_from_top = $(window).scrollTop();
            var speed = height_from_top / 3;
            $(window).scrollTop(height_from_top - speed);
            if (height_from_top === 0) {
                clearInterval(timer);
            }
        }, 10);
    });
});

