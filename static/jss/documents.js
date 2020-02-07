jQuery(document).ready(function() {
    $("form[name='documents']").validate({
        errorClass: 'my-error-class',
        rules: {
            document_category_id: 'required',
            name: {
                required : true,
                remote : {url: "/test_document", async:false}
            },
            title: 'required',
            content: 'required',
            file_upload: {
                extension :"docx|pdf|doc"
            },
           
        },
        messages: {
            document_category_id: 'This field is required.Select the type of document.',
            name: {
                required : "This field is required",
                remote : "Document with this name already exists.",
            },
            title: 'This field is required',
            content: 'This field is required',
            file_upload: {
                extension :'file should be in pdf,docx or doc format'
            },
            
            
            
        },
        submitHandler: function(form) {
        form.submit();
        toastr.success('Documents added successfully')

        }
    });
});

