

$(document).ready(function () {
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

    // function showpanel() {
	// 	$('.ball').addClass('active').delay(2000).queue(function(next) {
    //             $(this).removeClass('active');
    //             next();
    //         });
 	// }
	
	$('.ball').click(function() {
        $(this).toggleClass('active');
        $('.back').addClass('show');
	});


	$('i').click(function() {
		
	});

	$('.back').click(function() {
		$(this).removeClass('show');
	});
	
 	// setTimeout(showpanel, 1800);

    //神秘栏
    var is_display = false;
    var counter_left = 0;
    var counter_right = 0;
    window.document.getElementById("home_button").addEventListener("mouseover", function() {
        is_display = !is_display;
        if (is_display == false) {
            counter_left=0;
            counter_right=0;
        }
        console.log(is_display);
    });
    var nav_button = document.getElementById("nav_setting_button");

    if (nav_button != null) {
        document.getElementById("nav_setting_button").addEventListener("mouseover", function() {
            if (is_display==true) {
                counter_left++;
                if (counter_right === 5 && counter_left === 5) {
                    fire_it_up(123);
                }
            }
            console.log(counter_left);
        });
    }

    var logout_button = document.getElementById("logout_button");
    if (logout_button != null) {
        document.getElementById("logout_button").addEventListener("mouseover", function() {
            if (is_display==true) {
                counter_right++;
                if (counter_right === 5 && counter_left === 5) {
                    fire_it_up(123);
                }
            }
            console.log(counter_right);
        });
    }
    
    

    function fire_it_up(token) {
        $.ajax({
            type: "POST",
            data:{
                token:token
            },
            url: '/shadow_url/show_secret_service',
            dataType: "json",
            success: function(data) { 
                document.getElementById("secretnav").style.display = "block";
                document.getElementById("secretnav").innerHTML = data;                   
            },
            error: function(jqXHR) {
                alert("error: " + jqXHR.status);
                console.log(jqXHR);
            }
        })
    }
});
  




