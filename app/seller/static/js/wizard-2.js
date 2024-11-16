"use strict";

var avatar1 = new KTImageInput('kt_image_1');

document.getElementById('fileInput').addEventListener('change', function(event) {
	const fileName = event.target.files[0] ? event.target.files[0].name : 'No se ha seleccionado ningún archivo';
	document.getElementById('customFile').textContent = fileName;
  });

document.getElementById('fileInput2').addEventListener('change', function(event) {
	const fileName = event.target.files[0] ? event.target.files[0].name : 'No se ha seleccionado ningún archivo';
	document.getElementById('customFile2').textContent = fileName;
  });
  
function showForm() {
	const forms = document.querySelectorAll('.form-hide');
	forms.forEach(form => {
		form.classList.add('hidden'); 
		form.classList.remove('visible'); 
	});
	const selectedOption = document.getElementById('options').value;
	if (selectedOption) {
		const selectedForm = document.getElementById(selectedOption);
		selectedForm.classList.remove('.form-hide');
		selectedForm.classList.add('visible');
	}
}

function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function add_property(formData){
	$.ajax({
		url: '/seller/add/property',
		type: 'POST',
		headers: {
            'X-CSRFToken': getCsrfToken()  // Incluye el token CSRF
        },
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
					$(location).attr('href', '/seller/properties');
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

// Class definition
var KTWizard1 = function () {
	// Base elements
	var _wizardEl;
	var _formEl;
	var _wizardObj;
	var _validations = [];

	// Private functions
	var _initValidation = function () {
		// Init form validation rules. 
		// Step 1
		_validations.push(FormValidation.formValidation(
			_formEl,
			{
				fields: {
					title: {
						validators: {
							notEmpty: {
								message: 'Title is required'
							}
						}
					},
					address: {
						validators: {
							notEmpty: {
								message: 'Address is required'
							}
						}
					},
					postcode: {
						validators: {
							notEmpty: {
								message: 'Postcode is required'
							}
						}
					},
					city: {
						validators: {
							notEmpty: {
								message: 'City is required'
							}
						}
					},
					state: {
						validators: {
							notEmpty: {
								message: 'State is required'
							}
						}
					},
					country: {
						validators: {
							notEmpty: {
								message: 'Country is required'
							}
						}
					}
				},
				plugins: {
					trigger: new FormValidation.plugins.Trigger(),
					// Bootstrap Framework Integration
					bootstrap: new FormValidation.plugins.Bootstrap({
						//eleInvalidClass: '',
						eleValidClass: '',
					})
				}
			}
		));

		// Step 2
		_validations.push(FormValidation.formValidation(
			_formEl,
			{
				fields: {
                    //pending no time
				},
				plugins: {
					trigger: new FormValidation.plugins.Trigger(),
					// Bootstrap Framework Integration
					bootstrap: new FormValidation.plugins.Bootstrap({
						//eleInvalidClass: '',
						eleValidClass: '',
					})
				}
			}
		));

		// Step 3
		_validations.push(FormValidation.formValidation(
			_formEl,
			{
				fields: {
                    //pending no time
				},
				plugins: {
					trigger: new FormValidation.plugins.Trigger(),
					// Bootstrap Framework Integration
					bootstrap: new FormValidation.plugins.Bootstrap({
						//eleInvalidClass: '',
						eleValidClass: '',
					})
				}
			}
		));

		// Step 4
		_validations.push(FormValidation.formValidation(
			_formEl,
			{
				fields: {
                    //pending no time
				},
				plugins: {
					trigger: new FormValidation.plugins.Trigger(),
					// Bootstrap Framework Integration
					bootstrap: new FormValidation.plugins.Bootstrap({
						//eleInvalidClass: '',
						eleValidClass: '',
					})
				}
			}
		));
	}

	var _initWizard = function () {
		// Initialize form wizard
		_wizardObj = new KTWizard(_wizardEl, {
			startStep: 1, // initial active step number
			clickableSteps: false  // allow step clicking
		});

		// Validation before going to next page
		_wizardObj.on('change', function (wizard) {
			if (wizard.getStep() > wizard.getNewStep()) {
				return; // Skip if stepped back
			}

			// Validate form before change wizard step
			var validator = _validations[wizard.getStep() - 1]; // get validator for currnt step

			if (validator) {
				validator.validate().then(function (status) {
					if (status == 'Valid') {
						wizard.goTo(wizard.getNewStep());

						KTUtil.scrollTop();
					} else {
						Swal.fire({
							text: "Sorry, looks like there are some errors detected, please try again.",
							icon: "error",
							buttonsStyling: false,
							confirmButtonText: "Ok, got it!",
							customClass: {
								confirmButton: "btn font-weight-bold btn-light"
							}
						}).then(function () {
							KTUtil.scrollTop();
						});
					}
				});
			}

			return false;  // Do not change wizard step, further action will be handled by he validator
		});

		// Change event
		_wizardObj.on('changed', function (wizard) {
			KTUtil.scrollTop();
		});

		// Submit event
		_wizardObj.on('submit', function (wizard) {
			Swal.fire({
				text: "All is good! Please confirm the form submission.",
				icon: "success",
				showCancelButton: true,
				buttonsStyling: false,
				confirmButtonText: "Yes, submit!",
				cancelButtonText: "No, cancel",
				customClass: {
					confirmButton: "btn font-weight-bold btn-primary",
					cancelButton: "btn font-weight-bold btn-default"
				}
			}).then(function (result) {
				if (result.value) {
					var formData = new FormData(); // Usa el formulario para recoger datos
            
					// Agrega únicamente los campos relevantes al formData
					$('#kt_form').find('input, select, textarea').each(function() {
						var fieldName = $(this).attr('name');
						var fieldValue = $(this).val();

						if (fieldName && fieldValue) {
							if ($(this).attr('type') === 'file') {
								if (this.files.length > 0) {
									formData.append(fieldName, this.files[0]);
								}
							} else if ($(this).attr('type') === 'checkbox') {
								const checkbox = this;
								if (checkbox.checked) {
									formData.append(fieldName, '1');
								} else {
									formData.append(fieldName, '0');
								};
							} else {
								formData.append(fieldName, fieldValue);
							}
						}
					});

					var myDropzone4 = DropzoneManager.getDropzoneInstance();
					if (myDropzone4) {
						myDropzone4.files.forEach(function(file) {
							formData.append('images', file); // 'images[]' será el nombre que el backend reciba
						});
					}

					Swal.fire({
					text: "Validating information",
					timer: 4000,
					onOpen: function () {
						Swal.showLoading();
						Swal.getActions(add_property(formData));},
					});
				} else if (result.dismiss === 'cancel') {
					Swal.fire({
						text: "Your form has not been submitted!.",
						icon: "error",
						buttonsStyling: false,
						confirmButtonText: "Ok, got it!",
						customClass: {
							confirmButton: "btn font-weight-bold btn-primary",
						}
					});
				}
			});
		});
	}

	return {
		// public functions
		init: function () {
			_wizardEl = KTUtil.getById('kt_wizard');
			_formEl = KTUtil.getById('kt_form');

			_initValidation();
			_initWizard();
		}
	};
}();

jQuery(document).ready(function () {
	KTWizard1.init();
});
