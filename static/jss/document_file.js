jQuery(document).ready(function() {
    $("form[name='document_file']").validate({
        errorClass: 'my-error-class',
        rules: {
            file_upload: {
                required : true,
                extension :"docx|pdf|doc"
            },
           
        },
        messages: {
            file_upload: {
                required : "This field is required",
                extension :'file should be in pdf,docx or doc format'
            },
            
            
            
        },
        submitHandler: function(form) {
        form.submit();
        toastr.success('File added successfully')

        }
    });
});

