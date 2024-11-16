$('#exampleModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); 
    var id = button.data('id'); 
    $('#exampleModal .btn-primary').attr('onclick', 'check_token("'+ id + '")');
});

function check_token(id) {
    var formData = new FormData();
    formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val()); 
    formData.append("id", id);
    $('#kt_form').find('input, select, textarea').each(function() {
        var fieldName = $(this).attr('name');
        var fieldValue = $(this).val();

        if (fieldName && fieldValue) {
            if ($(this).attr('type') === 'checkbox') {
                const checkbox = this;
                if (checkbox.checked) {
                    formData.append(fieldName, 'True');
                } else {
                    formData.append(fieldName, 'False');
                };
            } else {
                formData.append(fieldName, fieldValue);
            }
        }
    });
    Swal.fire({
        title: "Are you sure you want to resale this token?",
        showCancelButton: true,
        confirmButtonText: "Confirm",
        cancelButtonText: "Cancel",
        reverseButtons: true
    }).then(function(result) {
        if (result.value) {
            // Si el usuario confirma, mostrar un mensaje de validación y llamar a buy_token
            Swal.fire({
                text: "Validating information",                                
                timer: 1000,
                onOpen: function() {
                    Swal.showLoading();
                }
            }).then(function() {
                // Llama a buy_token después de la validación
                resale_token(formData);
            });
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            // Si el usuario cancela, puedes ejecutar alguna acción opcional
            console.log("Compra cancelada");
        }
    });
}

function resale_token(formData) {
    $.ajax({
        url: '/marketplace/resale',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
    }).done(function(data) {
        var type = data.code == 200 ? "success" : "error";
        swal.fire({
            text: data.msg,
            icon: type,
            buttonsStyling: false,
            confirmButtonText: "OK",
            customClass: {
                confirmButton: "btn font-weight-bold btn-light-primary"
            },
            onClose: () => {
                $(location).attr('href', '/buyer/tokens');
            },
        }).then(function() {
            KTUtil.scrollTop();
        });
    });
}

