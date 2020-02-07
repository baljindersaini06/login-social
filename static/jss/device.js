jQuery(document).ready(function() {
    $("form[name='device']").validate({
        errorClass: 'my-error-class',
        rules: {
            device_type_id: 'required',
            location_id: 'required',
            device_name: 'required',
            device_url_address: {
                required : true,
                remote : {url: "/test_device_url", async:false}
            },
            device_note: 'required',
            device_configuration_id: 'required',
            device_configuration_parent_id: 'required',

           
        },
        messages: {
            device_type_id: 'This field is required',
            location_id: 'This field is required',
            device_name: 'This field is required',
            device_url_address: {
                required : "This field is required",
                remote : "Device with this url address already exists.",
            },
            device_note: 'This field is required',
            device_configuration_id: 'This field is required',
            device_configuration_parent_id: 'This field is required'
           
            
            
        },
        submitHandler: function(form) {
        form.submit();
        toastr.success('Device added successfully')

        }
    });
});

