jQuery(document).ready(function() {
    $("form[name='lice']").validate({
        errorClass: 'my-error-class',
        rules: {
            licence_type_id: 'required',
            licence_name: 'required',
            licence_quantity: 'required',
            licence_key: {
                required : true,
                remote : {url: "/test_licence_key", async:false}
            },
            aquisition_date: 'required',
            activation_date: 'required',
            expire_date: 'required',

           
        },
        messages: {
            licence_type_id: 'This field is required',
            licence_name: 'This field is required',
            licence_quantity: 'This field is required',
            licence_key: {
                required : "This field is required",
                remote : "Licence with this key already exists.",
            },
            aquisition_date: 'This field is required',
            activation_date: 'This field is required',
            expire_date: 'This field is required'
           
            
            
        },
        submitHandler: function(form) {
        form.submit();
        toastr.success('Licence added successfully')

        }
    });
});

