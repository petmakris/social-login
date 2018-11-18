
function pretty(obj) {
    return JSON.stringify(obj, null, 4).trim();
}

function showModal(title, body) {
    $('#modal-title').text(title);
    $('#modal-body').html(body);
    $('#info-modal').modal('show');
}

gapi.load('auth2', function () {
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
    FB.init({
        appId: facebook_client_id,
        cookie: true,
        xfbml: true,
        version: 'v2.8'
    });

    FB.getLoginStatus(function (statusResponse) {
        if (statusResponse['connected'] == true) {
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


$(function() {

    function responseHandler(isLogin, tokenDetails) {
        $.get('/token?', tokenDetails)
            .done(function (authResponse) {
                if (authResponse['connected'] == true) {
                    window.location.href = '/';
                } else {
                    if (isLogin) {
                            window.location.href = '/register?' + $.param(authResponse);
                    } else {
                        hideRegistrationElements();
                        configureSignupFormDetails(authResponse);
                    }
                }
            })
            .fail(function (err) {
                showModal('Failure', pretty(err));
            });
    }

    $('a.social-btn-google').click(function (e) {

        var isLoginBtn = $(this).hasClass('social-btn-login');
        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signIn().then(function () {
            var google_user = auth2.currentUser.get();
            var id_token = google_user.getAuthResponse().id_token;
            responseHandler(isLoginBtn, {'vendor': 'google', 'token': id_token})
        });

        e.preventDefault();
    })

    $('a.social-btn-facebook').click(function (e) {
        var isLoginBtn = $(this).hasClass('social-btn-login');
        var loginHandler = function (fbSigninResponse) {
            if (fbSigninResponse.status === 'connected') {
                var access_token = fbSigninResponse.authResponse.accessToken;
                responseHandler(isLoginBtn, {'vendor': 'facebook', 'token': access_token});
            }
        };
        var loginParams = {
            scope: 'public_profile,email'
        };
   
        FB.login(loginHandler, loginParams);
        e.preventDefault();
    })


    $('#signoutButton').click(function (e) {
        var auth2 = gapi.auth2.getAuthInstance();

        auth2.signOut().then(function () {
            $('.google-status i.fab').removeClass('text-success');
        });

        FB.getLoginStatus(function (statusResponse) {
            if (statusResponse['connected'] == true) {
                FB.logout(function (logoutResponse) {
                    $('.facebook-status i.fab').removeClass('text-success');
                })
            }
        });

        $.get('/logout');
        window.location.href = '/';
    });

    
    $("form#register").submit(function(e) {

        var action = $(this).attr('action');
        var data = $(this).serialize();

        $.get(action, data)
            .done(function(r) {
                if (r['connected'] == true) {
                    window.location.href = '/';
                }
                else {
                    showModal('Error', pretty(r));
                }
            })
            .fail(function(error) {
                showModal('Error', pretty(r));
            })

        e.preventDefault();
    });


    $('#show-users').click(function (e) {
        $.get('/getUsers')
            .then(function(r) {
                showModal('Users', pretty(r));
            })
        e.preventDefault();
    })


    $('#show-session').click(function (e) {
        $.get('/getSession')
            .then(function(r) { 
                showModal('Session', pretty(r));
            })
        e.preventDefault();
    })

    $('#show-model').click(function (e) {
        $.get('/getModel')
            .then(function(r) { 
                showModal('Model', pretty(r));
            })
        e.preventDefault();
    })

    $('#delete-user').click(function (e) {
        $.get('/deleteCurrentUser')
            .then(function(r) {
                if (r['deleted'] = true) {
                    window.location.href = '/';
                } else {
                    showModal('Error', pretty(r))
                }
            })
        e.preventDefault();
    })

})