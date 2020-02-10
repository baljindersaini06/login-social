jQuery(document).ready(function() {
    $("form[name='document_links']").validate({
        errorClass: 'my-error-class',
        rules: {
            links: {
                required : true,
               
            },
           
        },
        messages: {
            links: {
                required : "This field is required",
               
            },
            
            
            
        },
        submitHandler: function(form) {
        form.submit();
        toastr.success('File added successfully')

        }
    });
});

