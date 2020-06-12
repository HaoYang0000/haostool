

$(document).ready(function () {

    setTimeout(function(){
        $(".notify").toggleClass("active");
    },1000);

    setTimeout(function(){
        $(".notify").toggleClass("gone");
      },6000);
    //置顶栏
    var scrollTop = document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;;
    document.getElementById('goTopButton').onclick = function() {
        var timer = setInterval(function() {
            window.scrollBy(0, -100);
            if (scrollTop == 0) {
                clearInterval(timer);
            };
        }, 5);
    }

    //右下角工具栏
    window.onscroll = function() {
        scrollTop = document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;
    }
	
	$('.ball').click(function() {
        $(this).toggleClass('active');
        $('.back').addClass('show');
	});

	$('.back').click(function() {
		$(this).removeClass('show');
    });
    function append_script_to_dom(code) {
        var s = document.createElement('script');
        s.type = 'text/javascript';
        try {
            s.appendChild(document.createTextNode(code));
            document.body.appendChild(s);
        } catch (e) {
            s.text = code;
            document.body.appendChild(s);
        }
    }

    //神秘栏
    var first_try = true;
    var csrf_token = "sjakdljasksdjkla";
    window.document.getElementById("home_button").addEventListener("mouseover", function() {
        if (typeof fire_it_up !== "function" && first_try === true) {
            first_try = false;
            $.ajax({
                type: "POST",
                data:{
                    csrf_token:csrf_token
                },
                url: '/shadow_url/get_functions',
                dataType: "json",
                success: function(data) { 
                    append_script_to_dom(data.code);
                },
                error: () => {}
            });
        }
    });
});
  




