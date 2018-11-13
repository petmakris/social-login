var google_client_id = '';
var facebook_app_id = '';

function googleLoginInit() {
	gapi.load('auth2', function() {
		auth2 = gapi.auth2.init({
			client_id: google_client_id,
			fetch_basic_profile: true,
			scope: 'openid'
		});
	});
}

window.fbAsyncInit = function() {
	FB.init({
	appId   : facebook_app_id,
	cookie  : true,
	xfbml   : true,
	version : 'v2.8'
	});
};

function configureSignupFormDetails(auth) {

	$('form#signup div#social-buttons').hide();

	$('form#signup div.first_name').hide();
	$('form#signup div.last_name').hide();
	$('form#signup div.username').hide();

	$('form#signup span#welcome_message_1').text('Welcome ' + auth.first_name + ' ' + auth.last_name + '!');
	$('form#signup span#welcome_message_2').text('Please complete the following information to complete registration.');

	$('form#signup input#vid').val(auth.vid);
	$('form#signup input#vendor').val(auth.vendor);

	$('form#signup input#first_name').val(auth.first_name);
	$('form#signup input#last_name').val(auth.last_name);

	$('form#signup input#username').val(auth.email);


	$('form#signup input#picture').val(auth.picture);
}


function googleSigninRequest(callback) {
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signIn().then(function() {
		var google_user = auth2.currentUser.get();
		var id_token = google_user.getAuthResponse().id_token;
		callback(id_token);
	});
}

function facebookSigninRequest(callback) {
	FB.login(function(fbSigninResponse) {
		if (fbSigninResponse.status === 'connected') {
			var access_token = fbSigninResponse.authResponse.accessToken;
			callback(access_token);
		}
	}, {scope: 'public_profile,email'});
}

$().ready(function() {
    /*

	$('a.social-btn-google').click(function() {

		var isLoginBtn = $(this).hasClass('social-btn-login');
		var endUrl = $(this).attr('end-url');

		googleSigninRequest(function(id_token) {
			$.get('/cfc/users.cfc?method=handlegooglesignin', {'id_token': id_token})
				.done(function (authResponse) {
						if (authResponse.status == 'connected') {
							window.location.href = endUrl;
						} else {
							if (isLoginBtn) {
								window.location.href = '/sign_up/create_account?' + $.param(authResponse);
							} else {
								configureSignupFormDetails(authResponse);
							}
						}
					});
		})
	})

	$('a.social-btn-facebook').click(function() {

		var isLoginBtn = $(this).hasClass('social-btn-login');
		var endUrl = $(this).attr('end-url');

		facebookSigninRequest(function (access_token) {
			$.get('/cfc/users.cfc?method=handlefacebooksignin', {'accessToken': access_token})
				.done(function (authResponse) {
					if (authResponse.status == 'connected') {
						window.location.href = endUrl;
					} else {
						if (isLoginBtn) {
							window.location.href = '/sign_up/create_account?' + $.param(authResponse);
						} else {
							configureSignupFormDetails(authResponse);
						}
					}
				});
			})
	})

    */

	/*
	$('#signoutButton').click(function() {
		var auth2 = gapi.auth2.getAuthInstance();

		auth2.signOut().then(function () {
			console.log('google-sign-out');
		});

		FB.getLoginStatus(function(statusResponse) {
			if (statusResponse['status'] == 'connected') {
				FB.logout(function(logoutResponse) {
					console.log('facebook-sign-out', logoutResponse);
				})
			}
		});

		window.location.href = '/';
	});
	*/
})
