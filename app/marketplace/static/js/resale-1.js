function check_token(id) {
    var formData = new FormData($('#kt_form')[0]);
    formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val()); 
    formData.append("quantity", $('#touchspin').val());
    formData.append("id", id);
    Swal.fire({
        title: "Are you sure you want to buy these tokens?",
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
                buy_token(formData);
            });
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            // Si el usuario cancela, puedes ejecutar alguna acción opcional
            console.log("Compra cancelada");
        }
    });
}

function buy_token(formData) {
    $.ajax({
        url: '/buyer/buy',
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