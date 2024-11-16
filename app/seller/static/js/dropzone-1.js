"use strict";

var DropzoneManager = (function () {
    var myDropzone4;

    function initDropzone() {
        var id = '#kt_dropzone';
        var previewNode = $(id + " .dropzone-item");
        previewNode.id = "";
        var previewTemplate = previewNode.parent('.dropzone-items').html();
        previewNode.remove();

        myDropzone4 = new Dropzone(id, { 
            url: "/", // URL temporal, cambiar al endpoint adecuado
            parallelUploads: 20,
            previewTemplate: previewTemplate,
            maxFilesize: 4, 
            autoQueue: false,
            previewsContainer: id + " .dropzone-items",
            clickable: id + " .dropzone-select"
        });

        myDropzone4.on("addedfile", function(file) {
            file.previewElement.querySelector(id + " .dropzone-start").onclick = function() { 
                myDropzone4.enqueueFile(file); 
            };
            $(document).find(id + ' .dropzone-item').css('display', '');
            $(id + " .dropzone-remove-all").css('display', 'inline-block');
        });

        document.querySelector(id + " .dropzone-remove-all").onclick = function() {
            $(id + " .dropzone-upload, " + id + " .dropzone-remove-all").css('display', 'none');
            myDropzone4.removeAllFiles(true);
        };
    }

    return {
        init: function() {
            initDropzone();
        },
        getDropzoneInstance: function() {
            return myDropzone4;
        }
    };
})();

$(document).ready(function() {
    DropzoneManager.init();
});