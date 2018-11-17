var google_client_id = '315004607505-k9m58flrf24nrjdpqmbp5p6pfmfpmvvt.apps.googleusercontent.com';
var facebook_app_id = '341008546449852';


gapi.load('auth2', function () {

    console.log(':: google init()')
 
    auth2 = gapi.auth2.init({
        client_id: google_client_id,
        fetch_basic_profile: true,
        scope: 'openid'
    });
});


setTimeout(function() {
    if(gapi.auth2.getAuthInstance().isSignedIn.get()) {
        $('.google-status i.fab').addClass('text-success');
    }
}, 1000);


(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s);
    js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));


window.fbAsyncInit = function () {

    console.log(':: facebook init()')

    FB.init({
        appId: facebook_app_id,
        cookie: true,
        xfbml: true,
        version: 'v2.8'
    });

    FB.getLoginStatus(function (statusResponse) {
        if (statusResponse['status'] == 'connected') {
            $('.facebook-status i.fab').addClass('text-success');
        } 
    });

};

function hideRegistrationElements() {

    $('form#register div#social-buttons').hide();
    $('form#register div.first_name').hide();
    $('form#register div.last_name').hide();
    $('form#register div.email').hide();
    $('form#register div.password').hide();
    $('form#register input#password').val(Math.random().toString(36).slice(2));
}

function configureSignupFormDetails(auth) {

    $('form#register input#vid').val(auth.vid);
    $('form#register input#vendor').val(auth.vendor);
    $('form#register input#token').val(auth.token);
    $('form#register input#first_name').val(auth.first_name);
    $('form#register input#last_name').val(auth.last_name);
    $('form#register input#email').val(auth.email);
}


$().ready(function () {

    function handle(isLogin, tokenDetails) {
        $.get('/token?', tokenDetails)
            .done(function (authResponse) {
                console.log(authResponse)
                if (authResponse.status == 'connected') {
                    window.location.href = '/';
                } else {
                    if (isLogin) {
                            window.location.href = '/register?' + $.param(authResponse);
                    } else {
                        hideRegistrationElements();
                        configureSignupFormDetails(authResponse);
                    }
                }
            });
    }

    $('a.social-btn-google').click(function () {
        var isLoginBtn = $(this).hasClass('social-btn-login');

        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signIn().then(function () {
            var google_user = auth2.currentUser.get();
            var id_token = google_user.getAuthResponse().id_token;
            handle(isLoginBtn, {'vendor': 'google', 'token': id_token})
        });
    })

    $('a.social-btn-facebook').click(function () {

        var isLoginBtn = $(this).hasClass('social-btn-login');

        var loginHandler = function (fbSigninResponse) {
            if (fbSigninResponse.status === 'connected') {
                var access_token = fbSigninResponse.authResponse.accessToken;
                handle(isLoginBtn, {'vendor': 'facebook', 'token': access_token});
            }
        };
        var loginParams = {
            scope: 'public_profile,email'
        };
   
        FB.login(loginHandler, loginParams);
    })


    $('#signoutButton').click(function () {

        var auth2 = gapi.auth2.getAuthInstance();

        auth2.signOut().then(function () {
            $('.google-status i.fab').removeClass('text-success');
        });

        FB.getLoginStatus(function (statusResponse) {
            if (statusResponse['status'] == 'connected') {
                FB.logout(function (logoutResponse) {
                    $('.facebook-status i.fab').removeClass('text-success');
                })
            }
        });

        $.get('/logout');
        window.location.href = '/';

    });

    $("form#register").submit(function(e) {
        var form = $(this);
        $.ajax({
            type: "POST",
            url: form.attr('action'),
            data: form.serialize(),
            success: function(data) {
                console.log(data)
                }
            });
        e.preventDefault();
    });


    $("#dump").click(function(e) {
        $.get('/users').then(function(r) {
            console.log(r);
        })
        
        e.preventDefault();
    });


})
