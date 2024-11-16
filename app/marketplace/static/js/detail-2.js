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
            Swal.fire({
                text: "Validating information",                                
                timer: 1000,
                onOpen: function() {
                    Swal.showLoading();
                }
            }).then(function() {
                // Llama a buy_token después de la validación
                buy_resale_token(formData);
            });
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            // Si el usuario cancela, puedes ejecutar alguna acción opcional
            console.log("Compra cancelada");
        }
    });
}

function buy_resale_token(formData) {
    $.ajax({
        url: '/marketplace/transfer',
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


function offer_token(id) {
    var formData = new FormData();
    formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val()); 
    formData.append("offer_price", $('#offer_price').val());
    formData.append("id", id);
    console.log(formData);
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
                offer_token_send(formData);
            });
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            // Si el usuario cancela, puedes ejecutar alguna acción opcional
            console.log("Compra cancelada");
        }
    });
}

function offer_token_send(formData) {
    console.log(formData);
    $.ajax({
        url: '/marketplace/offer',
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
                location.reload();
            },
        }).then(function() {
            KTUtil.scrollTop();
        });
    });
}