var KTDatatableTranslationDemo = function() {
    // Private functions

    // basic demo
    var demo = function() {
            var datatable = $('#kt_datatable').KTDatatable({
                data: {
                    type: 'remote',
                    source:{
                        read: {
                            url: urls,
                        },
                    },
                    pageSize: 10,                    
                    serverPaging: true,
                    serverFiltering: true,
                },
                layout: {
                    scroll: true, 
                    footer: false,
                },

                sortable: true,

                pagination: true,
                search: {
                    input: $('#kt_datatable_search_query'),
                    key: 'generalSearch'
                },
                // columns definition
                columns: columnss,

                translate: {
                    records: {
                        processing: 'Loading...',
                        noRecords: 'Not matches found',
                    },
                    toolbar: {
                        pagination: {
                            items: {
                                default: {
                                    first: 'First',
                                    prev: 'Previous',
                                    next: 'Next',
                                    last: 'Last',
                                    more: 'More',
                                    input: 'Page number',
                                    select: 'SSelect page size',
                                },
                            },
                        },
                    },
                },
            });  

            
            $('#kt_datatable_search_user_id').on('change', function() {
                datatable.search($(this).val().toLowerCase(), 'UserID');
            }); 

            $('#kt_datepicker').datepicker({
                todayHighlight: true,
                templates: {
                    leftArrow: '<i class="la la-angle-left"></i>',
                    rightArrow: '<i class="la la-angle-right"></i>',
                },
            });

            //Loogbook
            $('#kt_datatable_search_action').on('change', function() {
                datatable.search($(this).val().toLowerCase(), 'Action');
            });   

        };

        return {
            // public functions
            init: function() {
                demo();
            },
        };
    }();

    jQuery(document).ready(function() {
        KTDatatableTranslationDemo.init();
    });
