jQuery(document).ready(function() {
    $('form[id="group"]').validate({
        errorClass: 'my-error-class',
        rules: {
            name: {
                required : true,
                remote : {url: "/test_group", async:false}
            }
        },
        messages: {
            name: {
                required : "This field is required",
                remote : "Group with this name is already present.",
            }
            
        },
        submitHandler: function(form) {
        form.submit();
        toastr.success('Group added successfully')

        }
    });
});

