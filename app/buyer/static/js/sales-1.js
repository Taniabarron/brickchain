function canceResale(id) {
    console.log(id);
    var formData = new FormData();
    formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val()); 
    formData.append("id", id);
  
    $.ajax({
        url: '/buyer/cancel/resale',
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
  
var urls = '/buyer/get_resale';
var columnss = [{
        field: 'Property',
        title: 'Property',
    },{
        field: 'Cost',
        title: 'Cost',
    },{
        field: 'Publish',
        title: 'Publish Price',
    },{
        field: 'IdChain',
        title: 'Chain ID',
    },{
        field: 'Status',
        title: 'Status',
    },{
        field: 'Auction',
        title: 'Auction',
    },{
        field: 'ShipDate',
        title: 'Sale Date',
        textAlign: 'center',
    },{
		field: 'Actions',
		title: 'Actions',
		sortable: false,
		width: 130,
		overflow: 'visible',
	    autoHide: false,
		template: function(row) {
						return '\
	                        <a id="edit-user" href="/marketplace/detail/'+row.ResaleID+'" class="btn btn-sm btn-default btn-text-primary btn-hover-primary btn-icon mr-2" title="Edit details">\
	                            <span class="svg-icon svg-icon-md">\
                                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1">\
                                        <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">\
                                            <rect x="0" y="0" width="24" height="24"/>\
											<path d="M3,12 C3,12 5.45454545,6 12,6 C16.9090909,6 21,12 21,12 C21,12 16.9090909,18 12,18 C5.45454545,18 3,12 3,12 Z" fill="#000000" fill-rule="nonzero" opacity="0.3"/>\
											<path d="M12,15 C10.3431458,15 9,13.6568542 9,12 C9,10.3431458 10.3431458,9 12,9 C13.6568542,9 15,10.3431458 15,12 C15,13.6568542 13.6568542,15 12,15 Z" fill="#000000" opacity="0.3"/>\
										</g>\
									</svg>\
	                            </span>\
	                        </a>\
                            <button '+row.Action+' onclick="canceResale('+row.RecordID+');" class="btn btn-sm btn-clean btn-icon" title="Cancel">\
                                <span class="svg-icon svg-icon-md">\
                                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1">\
                                        <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">\
                                            <rect x="0" y="0" width="24" height="24"/>\
                                            <path d="M6,8 L6,20.5 C6,21.3284271 6.67157288,22 7.5,22 L16.5,22 C17.3284271,22 18,21.3284271 18,20.5 L18,8 L6,8 Z" fill="#000000" fill-rule="nonzero"/>\
                                            <path d="M14,4.5 L14,4 C14,3.44771525 13.5522847,3 13,3 L11,3 C10.4477153,3 10,3.44771525 10,4 L10,4.5 L5.5,4.5 C5.22385763,4.5 5,4.72385763 5,5 L5,5.5 C5,5.77614237 5.22385763,6 5.5,6 L18.5,6 C18.7761424,6 19,5.77614237 19,5.5 L19,5 C19,4.72385763 18.7761424,4.5 18.5,4.5 L14,4.5 Z" fill="#000000" opacity="0.3"/>\
                                        </g>\
                                    </svg>\
                                </span>\
                            </button>\ ';
					},
}]