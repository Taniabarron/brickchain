$(document).ready(function() {
    // TouchSpin initialization for the quantity field
    $('#touchspin').TouchSpin({
        buttondown_class: 'btn btn-secondary btn-sm',
        buttonup_class: 'btn btn-secondary btn-sm',
        min: 0,
        step: 1,
        boostat: 4,
        maxboostedstep: 10
    });

    // Function to calculate the subtotal
    function updateSubtotal() {
        // We obtain the value of quantity and cost
        var quantity = parseInt($('#touchspin').val()) || 0; // f the value is NaN, use 0
        var cost = parseFloat($('#cost').text().replace('$', '').trim()) || 0;

        // Calculate the subtotal and update it in the corresponding field
        var subtotal = quantity * cost;
        $('#subtotal').text(`$${subtotal.toFixed(2)}`);
    }

    // Listen for changes in quantity to update the subtotal
    $('#touchspin').on('change', updateSubtotal);

    // Initialize subtotal on page load
    updateSubtotal();
});

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