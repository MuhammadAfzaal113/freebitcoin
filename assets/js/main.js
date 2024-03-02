
$(document).ready(function() {

    // Code to pause and play loader
    function playLoader(){
        $('#loader_container').addClass('active')
        $('#loader_span').addClass('play')
    }
    function stopLoader(){
        $('#loader_container').removeClass('active')
        $('#loader_span').removeClass('play')
    }


    function destroyPopup() {
        $('.popup-background').fadeOut(200, function() {
            $(this).remove();
        })
    }

    function createPopup(header,content) {
        $('main').eq(0).after(
            $('<div>').addClass('popup-background').append(
                $('<div>').addClass('popup-container').append(
                    $('<div>').addClass('popup-wrapper').append(
                        $('<div>').addClass('popup-controls').append(
                            $('<span>').addClass('popup-close fa fa-remove bg-1')
                        )
                    ).append(
                        $('<div>').addClass('popup-content').append(
                            $('<h1>').addClass('color-1').html(header)
                        ).append(
                            $('<div>').addClass('popup-inner-content').html(content)
                        )
                    )
                )
            )
        );

        $('.popup-background').fadeIn();
    }

    $(document).mouseup(function(e) {
        var container = $(".popup-wrapper");

        // if the target of the click isn't the container nor a descendant of the container
        if (!container.is(e.target) && container.has(e.target).length === 0) 
        {
            destroyPopup();
        }
    });

    if ($(window).width() > 768) {
        $('ul.nav li.dropdown').hover(function() {
            $(this).find('ul.dropdown-menu').css('display', 'block');
        }, function() {
            $(this).find('ul.dropdown-menu').css('display','none');
        });

        $('.dropdown > a').removeClass('dropdown-toggle').attr('data-toggle','');
    }


    $('.alert').not('.alert-important').delay(5000).slideUp(300);


    $(document).on('click', '.popup-close,.popup-cancel', function( e ) {
        e.preventDefault();
        destroyPopup();
    });



    function commaSeparateNumber(val) {
        while (/(\d+)(\d{3})/.test(val.toString())) {
            val = val.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
        }
        return val;
    }

    function scrollTo(elem) {
        $('html, body').animate({
            scrollTop: $(elem).offset().top
        }, 1000);
    }

    function resetError() {
        $('.error').text('').hide();
    }

    function hash(text) {
        var md5 = function(s){function L(k,d){return(k<<d)|(k>>>(32-d))}function K(G,k){var I,d,F,H,x;F=(G&2147483648);H=(k&2147483648);I=(G&1073741824);d=(k&1073741824);x=(G&1073741823)+(k&1073741823);if(I&d){return(x^2147483648^F^H)}if(I|d){if(x&1073741824){return(x^3221225472^F^H)}else{return(x^1073741824^F^H)}}else{return(x^F^H)}}function r(d,F,k){return(d&F)|((~d)&k)}function q(d,F,k){return(d&k)|(F&(~k))}function p(d,F,k){return(d^F^k)}function n(d,F,k){return(F^(d|(~k)))}function u(G,F,aa,Z,k,H,I){G=K(G,K(K(r(F,aa,Z),k),I));return K(L(G,H),F)}function f(G,F,aa,Z,k,H,I){G=K(G,K(K(q(F,aa,Z),k),I));return K(L(G,H),F)}function D(G,F,aa,Z,k,H,I){G=K(G,K(K(p(F,aa,Z),k),I));return K(L(G,H),F)}function t(G,F,aa,Z,k,H,I){G=K(G,K(K(n(F,aa,Z),k),I));return K(L(G,H),F)}function e(G){var Z;var F=G.length;var x=F+8;var k=(x-(x%64))/64;var I=(k+1)*16;var aa=Array(I-1);var d=0;var H=0;while(H<F){Z=(H-(H%4))/4;d=(H%4)*8;aa[Z]=(aa[Z]| (G.charCodeAt(H)<<d));H++}Z=(H-(H%4))/4;d=(H%4)*8;aa[Z]=aa[Z]|(128<<d);aa[I-2]=F<<3;aa[I-1]=F>>>29;return aa}function B(x){var k="",F="",G,d;for(d=0;d<=3;d++){G=(x>>>(d*8))&255;F="0"+G.toString(16);k=k+F.substr(F.length-2,2)}return k}function J(k){k=k.replace(/rn/g,"n");var d="";for(var F=0;F<k.length;F++){var x=k.charCodeAt(F);if(x<128){d+=String.fromCharCode(x)}else{if((x>127)&&(x<2048)){d+=String.fromCharCode((x>>6)|192);d+=String.fromCharCode((x&63)|128)}else{d+=String.fromCharCode((x>>12)|224);d+=String.fromCharCode(((x>>6)&63)|128);d+=String.fromCharCode((x&63)|128)}}}return d}var C=Array();var P,h,E,v,g,Y,X,W,V;var S=7,Q=12,N=17,M=22;var A=5,z=9,y=14,w=20;var o=4,m=11,l=16,j=23;var U=6,T=10,R=15,O=21;s=J(s);C=e(s);Y=1732584193;X=4023233417;W=2562383102;V=271733878;for(P=0;P<C.length;P+=16){h=Y;E=X;v=W;g=V;Y=u(Y,X,W,V,C[P+0],S,3614090360);V=u(V,Y,X,W,C[P+1],Q,3905402710);W=u(W,V,Y,X,C[P+2],N,606105819);X=u(X,W,V,Y,C[P+3],M,3250441966);Y=u(Y,X,W,V,C[P+4],S,4118548399);V=u(V,Y,X,W,C[P+5],Q,1200080426);W=u(W,V,Y,X,C[P+6],N,2821735955);X=u(X,W,V,Y,C[P+7],M,4249261313);Y=u(Y,X,W,V,C[P+8],S,1770035416);V=u(V,Y,X,W,C[P+9],Q,2336552879);W=u(W,V,Y,X,C[P+10],N,4294925233);X=u(X,W,V,Y,C[P+11],M,2304563134);Y=u(Y,X,W,V,C[P+12],S,1804603682);V=u(V,Y,X,W,C[P+13],Q,4254626195);W=u(W,V,Y,X,C[P+14],N,2792965006);X=u(X,W,V,Y,C[P+15],M,1236535329);Y=f(Y,X,W,V,C[P+1],A,4129170786);V=f(V,Y,X,W,C[P+6],z,3225465664);W=f(W,V,Y,X,C[P+11],y,643717713);X=f(X,W,V,Y,C[P+0],w,3921069994);Y=f(Y,X,W,V,C[P+5],A,3593408605);V=f(V,Y,X,W,C[P+10],z,38016083);W=f(W,V,Y,X,C[P+15],y,3634488961);X=f(X,W,V,Y,C[P+4],w,3889429448);Y=f(Y,X,W,V,C[P+9],A,568446438);V=f(V,Y,X,W,C[P+14],z,3275163606);W=f(W,V,Y,X,C[P+3],y,4107603335);X=f(X,W,V,Y,C[P+8],w,1163531501);Y=f(Y,X,W,V,C[P+13],A,2850285829);V=f(V,Y,X,W,C[P+2],z,4243563512);W=f(W,V,Y,X,C[P+7],y,1735328473);X=f(X,W,V,Y,C[P+12],w,2368359562);Y=D(Y,X,W,V,C[P+5],o,4294588738);V=D(V,Y,X,W,C[P+8],m,2272392833);W=D(W,V,Y,X,C[P+11],l,1839030562);X=D(X,W,V,Y,C[P+14],j,4259657740);Y=D(Y,X,W,V,C[P+1],o,2763975236);V=D(V,Y,X,W,C[P+4],m,1272893353);W=D(W,V,Y,X,C[P+7],l,4139469664);X=D(X,W,V,Y,C[P+10],j,3200236656);Y=D(Y,X,W,V,C[P+13],o,681279174);V=D(V,Y,X,W,C[P+0],m,3936430074);W=D(W,V,Y,X,C[P+3],l,3572445317);X=D(X,W,V,Y,C[P+6],j,76029189);Y=D(Y,X,W,V,C[P+9],o,3654602809);V=D(V,Y,X,W,C[P+12],m,3873151461);W=D(W,V,Y,X,C[P+15],l,530742520);X=D(X,W,V,Y,C[P+2],j,3299628645);Y=t(Y,X,W,V,C[P+0],U,4096336452);V=t(V,Y,X,W,C[P+7],T,1126891415);W=t(W,V,Y,X,C[P+14],R,2878612391);X=t(X,W,V,Y,C[P+5],O,4237533241);Y=t(Y,X,W,V,C[P+12],U,1700485571);V=t(V,Y,X,W,C[P+3],T,2399980690);W=t(W,V,Y,X,C[P+10],R,4293915773);X=t(X,W,V,Y,C[P+1],O,2240044497);Y=t(Y,X,W,V,C[P+8],U,1873313359);V=t(V,Y,X,W,C[P+15],T,4264355552);W=t(W,V,Y,X,C[P+6],R,2734768916);X=t(X,W,V,Y,C[P+13],O,1309151649);Y=t(Y,X,W,V,C[P+4],U,4149444226);V=t(V,Y,X,W,C[P+11],T,3174756917);W=t(W,V,Y,X,C[P+2],R,718787259);X=t(X,W,V,Y,C[P+9],O,3951481745);Y=K(Y,h);X=K(X,E);W=K(W,v);V=K(V,g)}var i=B(Y)+B(X)+B(W)+B(V);return i.toLowerCase()};

        var hash = md5(text);
        return hash;
    }

    // Codes for ajax setup for get and post requests to backend
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    let csrftoken = getCookie('csrftoken');


    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }



    try{
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    } catch(e){
    }

    function findGetParameter(parameterName) {
        var result = null,
            tmp = [];
        var items = location.search.substr(1).split("&");
        for (var index = 0; index < items.length; index++) {
            tmp = items[index].split("=");
            if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        }
        return result;
    }


    function submitForm(e) {
        e.preventDefault()
        let form = this
        let formData = $(this).serialize();
        
        // Get the next parameter if it exists
        let next_get = findGetParameter('next')
        if (next_get){
            formData = formData + "&next=" + next_get
        }

        let thisURL = form.action

        // Play loader
        playLoader()

        $.ajax({
            method: "POST",
            url: thisURL,
            data: formData,
            success: function (data){
                if (data.redirect){
                    window.location.href = data['redirect'];
                }
            },
            error: function (jqXHR) {
                if (jqXHR.status == 403){
                    window.location.reload()
                }
                $('.form-errors').html('');
                for (const [key, value] of Object.entries(jqXHR['responseJSON'])) {
                    if (key != '__all__'){

                        if (key == 'hcaptcha'){
                            let input = form.querySelector('#hcaptcha-errors')
                            let new_el = document.createElement('small')
                            new_el.classList.add('text-danger')
                            new_el.innerText = value
                            input.appendChild(new_el)
                        } else {
                            let input = form.querySelector(".form-control[name='" + key + "']")
                            let new_el = document.createElement('small')
                            new_el.classList.add('text-danger')
                            new_el.innerText = value
                            input.nextElementSibling.appendChild(new_el)
                        }
                        
                    }
                }
            },
            complete: function () {
                stopLoader()
            }
        })
    }


    if($('.register-login').length){
        $('#login_form').submit(submitForm);
        
        $('#register_form').submit(submitForm);
        
        $('#forget_form').submit(submitForm);


        $('.login-link').click(function(e) {
            e.preventDefault();
            $('.login-wrapper').show();
            $('.register-wrapper').hide();
            $('.forgot-wrapper').hide();
        });

        $('.register-link').click(function(e) {
            e.preventDefault();
            $('.register-wrapper').show();
            $('.login-wrapper').hide();
            $('.forgot-wrapper').hide();
        });

        $('.forgot-link').click(function(e) {
            e.preventDefault();
            $('.forgot-wrapper').show();
            $('.register-wrapper').hide();
            $('.login-wrapper').hide();
        });
    }
    
    $('a').click(function(e) {
        if ($(this).attr('data-scroll')) {
            e.preventDefault();
            scrollTo('.' + $(this).attr('data-scroll'));    
        }
    });



    // Faq page script

    if ($('.faq-question').length){
        $('.faq-question').click(function() {
            if ($(this).is('.active')){
                $(this).closest('.faq-line-wrapper').find('.faq-answer').animate({'height':'0'},500,'linear',function() {
    
                });
                $(this).removeClass('active');
                $(this).find('.faq-expension').removeClass('fa-minus').addClass('fa-plus');
    
            }else{
                $(this).closest('.faq-line-wrapper').find('.faq-answer').css('height','auto').hide();
                var height = (parseInt($(this).closest('.faq-line-wrapper').find('.faq-answer').css('height').replace('px',''))) + 10 + 'px';
    
                $(this).closest('.faq-line-wrapper').find('.faq-answer').css({'height':'0'}).show();
                $(this).closest('.faq-line-wrapper').find('.faq-answer').animate({'height':height},500);
                $(this).addClass('active');
                $(this).find('.faq-expension').removeClass('fa-plus').addClass('fa-minus');
            }
        });
    }



    var roll_interval, time_interval;

    function getTimeRemaining(endtime) {
        var t = Date.parse(endtime) - Date.parse(new Date());
        var seconds = Math.floor((t / 1000) % 60);
        var minutes = Math.floor((t / 1000 / 60) % 60);
        return {
            'total': t,
            'minutes': minutes,
            'seconds': seconds
        };
    }

    function activateRollBtn(){
        $(".free .roll-wrapper").show();
        $(".roll-button").show();
        $(".free .timeout-wrapper").hide();
        clearInterval(time_interval);
    }

    function initializeClock(remaining_seconds) {
        var deadline = new Date();
        deadline.setMinutes(deadline.getMinutes() + remaining_seconds / 60);
        deadline.setSeconds(deadline.getSeconds() + remaining_seconds % 60);

        function updateClock() {
            var t = getTimeRemaining(deadline);
            $('.free .minutes .digits').text(t.minutes).slice(-2);
            $('.free .seconds .digits').text(t.seconds).slice(-2);

            if (t.total <= 0) {
                activateRollBtn();
                ringBell();
            }
        }

        updateClock();
        time_interval = setInterval(updateClock, 1000);
    }

    function getRandNum(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function ringBell() {
        var audio = new Audio('/static/ring.wav');
        audio.play()
    }

    function Counter() {
        function roll() {
            $('.free .digit-1').text(getRandNum(0, 9));
            $('.free .digit-2').text(getRandNum(0, 9));
            $('.free .digit-3').text(getRandNum(0, 9));
            $('.free .digit-4').text(getRandNum(0, 9));
            $('.free .digit-5').text(getRandNum(0, 9));
        }

        roll_interval = setInterval(roll, 30);
    }

    function pad(str, max) {
        str = str.toString();
        return str.length < max ? pad("0" + str, max) : str;
    }

    function setResult(result) {
        var lucky_number = pad(result.lucky_number.toString(), 5);

        if (result.pending_rolls > 0) {
            $(".pending-rolls").text("Rolls left: " + result.pending_rolls);
            $(".roll-button").show();
        } else {
            $(".pending-rolls").hide();
            $(".free .timeout-wrapper").show();

            initializeClock(result.remaining_seconds);
        }

        clearInterval(roll_interval);

        $('.free .digit-1').text(parseInt(lucky_number.charAt(0)));
        $('.free .digit-2').text(parseInt(lucky_number.charAt(1)));
        $('.free .digit-3').text(parseInt(lucky_number.charAt(2)));
        $('.free .digit-4').text(parseInt(lucky_number.charAt(3)));
        $('.free .digit-5').text(parseInt(lucky_number.charAt(4)));

        $('.result').text("You have received " + result.coins_won + ' OMI');
        $('.result').show();

        $(".navbar-coins a").text(result.total_coins + " OMI")
    }

    function rollClick() {    
        $.ajax({
            type: "POST",
            url: window.location.href,
            success: function (data) {
                setTimeout(function() {
                    setResult(data)
                }, 2000);

                console.log(data)

                let { first } = data
                if (first){
                    $("#lauchEarnMore").click()
                }
            },
            error: function(data){
                clearInterval(roll_interval);
                $('.free .digit-1').text(0);
                $('.free .digit-2').text(0);
                $('.free .digit-3').text(0);
                $('.free .digit-4').text(0);
                $('.free .digit-5').text(0);
            }
        });
    }
    
    let rem_time = document.getElementById('remaining_time')
    if (rem_time != null){
        var remainingSeconds = parseInt(rem_time.textContent);
        if (remainingSeconds > 0) {
            $(".free .roll-wrapper").hide();
            $(".free .timeout-wrapper").show();
            initializeClock(remainingSeconds);
        } else {
            $(".free .roll-wrapper").show();
            $(".free .timeout-wrapper").hide();
        }
    }
    

    $(".free .roll-button").click(function () {
        $(this).hide();
        $('.result').hide();

        Counter();

        rollClick();
    });

    $('.free .submit-promo').click(function() {
        let input = $(this).closest('.input-group').find('input');
        let input_value = input.val();
        let url = $(input).attr('data-url');
        submitPromoCode(input_value, url);
        input.val('');
    });


    // Submit promo code
    function submitPromoCode(value, url) {
        let formData = "code=" + value;

        playLoader()

        $.ajax({
            method: "POST",
            url: url,
            data: formData,
            success: function (data){
                activateRollBtn();
            },
            error: function (jqXHR) {
            },
            complete: function(jqXHR) {
                stopLoader()
                alert(jqXHR.responseJSON.message)
            }
        })
    }


    // Select tab
    function getTab(tab) {  
        let formData = "tab=" + tab;

        playLoader()

        $.ajax({
            type: "POST",
            url: window.location.href,
            data: formData,
            success: function (data){
                let content = data['content']
                $('.offerwalls-output').html(content)
            },
            error: function (jqXHR) {
            },
            complete: function(jqXHR) {
                stopLoader()
            }
        });
    }

    if ($('.iframe-wrapper a.link').length){
        $('.iframe-wrapper a.link').click(function(e){
            let tab = $(this).attr('data-tab')
            getTab(tab)
        })
    }

    if ($('#redeemModal form label p').length){
        $('#redeemModal form label p').click(function(e){
            let amount = $(this).attr('data-amount')
            $('#redeemModal form input').val(parseFloat(amount))
        })
    }


    function submitRedeem(e) {
        e.preventDefault()
        let form = this
        let formData = $(this).serialize();
        let thisURL = form.action

        // Play loader
        playLoader()

        $.ajax({
            method: "POST",
            url: thisURL,
            data: formData,
            success: function (data){
                alert(data['message'])
                window.location.reload()
            },
            error: function ({ responseJSON }) {
                let msg = responseJSON['message']
                $("#redeemModal form .text-danger").text(msg)
            },
            complete: function () {
                stopLoader()
            }
        })
    }

    if ($('#redeemModal form').length){
        $('#redeemModal form').unbind('submit').submit(submitRedeem);
    }

    function updateWithdrawalAmount(e){
        let amount_val = $('#WithdrawAmountID').val()
        amount_val = amount_val !== "" ? amount_val : "0";
        $("#WithdrawAmountView").text(amount_val)
    }

    if ($('#WithdrawAmountID').length){
        $('#WithdrawAmountID').keyup(updateWithdrawalAmount)
        $('#WithdrawAmountID').keydown(updateWithdrawalAmount)
    }
    
});