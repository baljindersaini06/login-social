jQuery(document).ready(function() {
    $("form[name='website']").validate({
        errorClass: 'my-error-class',
        rules: {
            website_type: 'required',
            website_name: {
                required : true,
                remote : {url: "/test_website", async:false}
            },
            website_url: {
                required : true,
                remote : {url: "/test_website_url", async:false}
            },
           
        },
        messages: {
            website_type: 'This field is required',
            website_name: {
                required : "This field is required.",
                remote : "Website with this name already exists.",
            },
            website_url: {
                required : "Enter valid url of this website.",
                remote : "This website url already exists.",
            },
            
        },
        submitHandler: function(form) {
        form.submit();
        toastr.success('Website added successfully')

        }
    });
});

