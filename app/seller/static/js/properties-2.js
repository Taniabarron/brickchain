function onSwitch(checkbox, id) {
    const isChecked = checkbox.checked;
    var formData = new FormData();
    formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val()); 
    formData.append("checkbox", isChecked);
    formData.append("id", id);
  
    $.ajax({
        url: '/seller/status',
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

function search(fechaSearch = null) {
  let sear = $("#search").val().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  let propertyType = $("#propertyType").val();
  let dataNew = [];

  $(".card-doc").remove();
  console.log("Buscando:", sear, "Tipo:", propertyType, "Fecha:", fechaSearch);

  data.forEach(function(element) {
      // Filtro por título
      let matchesTitle = element.Title.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").includes(sear);
      
      // Filtro por tipo de propiedad
      let matchesType = (propertyType === "All" || element.Type === propertyType);

      // Filtro por fecha
      let matchesDate = true;
      if (fechaSearch != null && !isNaN(fechaSearch)) {
          let formattedDate = (fechaSearch.getDate() + 1).toString().padStart(2, '0') + "/" + 
                              (fechaSearch.getMonth() + 1).toString().padStart(2, '0') + "/" + 
                              fechaSearch.getFullYear();
          matchesDate = (element.CreateDate === formattedDate);
      }

      // Si el elemento cumple con todos los filtros, lo agregamos
      if (matchesTitle && matchesType && matchesDate) {
          appendMosaic(element);
          dataNew.push(element);
      }
  });
}

$(document).ready(function() {
  // Filtro por título
  $("#search").on("keyup", () => {
      let inputDate = new Date($("#kt_datepiker_pk1").val());
      search(inputDate);
  });

  // Filtro por fecha
  $("#kt_datepiker_pk1").change(function() {
      let inputDate = new Date(this.value);
      search(inputDate);
  });

  // Filtro por tipo de propiedad
  $("#propertyType").change(function() {
      let inputDate = new Date($("#kt_datepiker_pk1").val());
      search(inputDate);
  });
});