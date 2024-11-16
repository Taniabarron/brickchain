"use strict";
function password(formData){
	$.ajax({
		url: '/core/reset_password/confirm',
		type: 'POST',
		data: formData,
		contentType: false,
		processData: false,
	}).done(function (data){
		if (data.code == 200 ){
			swal.fire({
				text: data.msg,
				icon: 'success',
				buttonsStyling: false,
				confirmButtonText: "OK",
				customClass: {
					confirmButton: "btn font-weight-bold btn-light-primary"
				},
				onClose: () => {
					$(location).attr('href', '/');
				},
			}).then(function() {
				KTUtil.scrollTop();
			});
		}
		else{
			swal.fire({
				text: data.msg,
				icon: "error",
				buttonsStyling: false,
				confirmButtonText: "OK",
				customClass: {
					confirmButton: "btn font-weight-bold btn-light-primary"
				},
			}).then(function() {
				KTUtil.scrollTop();
			});
		}
	});
}

// Class Definition
var KTLogin = function() {
    var _login;

    var _showForm = function(form) {
        var cls = 'login-' + form + '-on';
        var form = 'kt_login_' + form + '_form';

        _login.removeClass('login-forgot-on');
        _login.removeClass('login-signin-on');
        _login.removeClass('login-signup-on');

        _login.addClass(cls);

        KTUtil.animateClass(KTUtil.getById(form), 'animate__animated animate__backInUp');
    }

    var _handlePasswordInForm = function() {
        var validation;

        validation = FormValidation.formValidation(
			KTUtil.getById('kt_login_password_form'),
			{
				fields: {
					password: {
						validators: {
							notEmpty: {
								message: 'Password is required'
							}
						}
					},
					cpassword: {
                        validators: {
                            notEmpty: {
                                message: 'The password confirmation is required'
                            },
                            identical: {
                                compare: function() {
                                    return form.querySelector('[name="password"]').value;
                                },
                                message: 'The password and its confirm are not the same'
                            }
                        }
                    },
				},
				plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    submitButton: new FormValidation.plugins.SubmitButton(),
                	bootstrap: new FormValidation.plugins.Bootstrap()
				}
			}
		);

        $('#kt_login_password_submit').on('click', function (e) {
            e.preventDefault();

            validation.validate().then(function(status) {
		        if (status == 'Valid') {
					var formData = new FormData($('#kt_login_password_form')[0]);
					Swal.fire({
					text: "Validating information",
					timer: 4000,
					onOpen: function () {
						Swal.showLoading();
						Swal.getActions(password(formData));},
					});
				} else {
					swal.fire({
		                text: "Sorry, looks like there are some errors detected, please try again.",
		                icon: "error",
		                buttonsStyling: false,
		                confirmButtonText: "Ok, got it!",
                        customClass: {
    						confirmButton: "btn font-weight-bold btn-light-primary"
    					}
		            }).then(function() {
						KTUtil.scrollTop();
					});
				}
		    });
        });
        // Handle forgot button
        $('#kt_login_forgot').on('click', function (e) {
            e.preventDefault();
            _showForm('forgot');
        });

    }

    // Public Functions
    return {
        // public functions
        init: function() {
            _login = $('#kt_login');

            _handlePasswordInForm();

        }
    };
}();

// Class Initialization
jQuery(document).ready(function() {
    KTLogin.init();
});