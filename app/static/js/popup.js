$(window).load(function () {
    $(".popup_trigger").click(function(){
       $('.popup_content').show();
    });

    $('.popup_close').click(function(){
        $('.popup_content').hide();
    });
});