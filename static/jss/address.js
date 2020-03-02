jQuery(document).ready(function() {
    $('form[name="address"]').validate({
        errorClass: 'my-error-class',
        rules: {
            location_name:{
                required : true,
                remote : {url: "/test_location", async:false}
            },

            location_address: {
                required : true,
                maxlength : 100,
            },
            location_city: {
                required : true,
                maxlength : 20,
            },
            location_postal_code: {
                required : true,
                maxlength : 6,
            },
            country: {
                required : true,
            },
            location_bussiness_hours: {
                required : false,
                maxlength : 24,
            }
          

        },
        messages: {
            location_name:{
                required : "This field is required",
                remote : "Location with this name already exists.",
            },
            location_address :{
                required : 'This field is required',
                maxlength : 'only 100 characters are allowed'
            },
            location_city: 'This field is required',
            location_postal_code: {
                required: "This field is required",
                maxlength: "Pincode can only contains 6 digits"
              },
            countries: {
                required :"This field is required",
            },
            location_bussiness_hours: {
                
                maxlength :"limit of 24hrs",
            }
            
        },
        submitHandler: function(form) {
        form.submit();
        toastr.success('Location added successfully')

        }
    });
});



jQuery(document).ready(function() {
    $('form[name="address_update"]').validate({
        errorClass: 'my-error-class',
        rules: {
            location_name:{
                required : true,
              
            },

            location_address: {
                required : true,
                maxlength : 100,
            },
            location_city: {
                required : true,
                maxlength : 20,
            },
            location_postal_code: {
                required : true,
                maxlength : 6,
            },
            country: {
                required : true,
            },
            location_bussiness_hours: {
                required : false,
                maxlength : 24,
            },
            // is_headquater:{
            //     remote : {url: "/test_location_update", async:false}
            // }

        },
        messages: {
            location_name:{
                required : "This field is required",
               
            },
            location_address :{
                required : 'This field is required',
                maxlength : 'only 100 characters are allowed'
            },
            location_city: 'This field is required',
            location_postal_code: {
                required: "This field is required",
                maxlength: "Pincode can only contains 6 digits"
              },
            countries: {
                required :"This field is required",
            },
            location_bussiness_hours: {
                
                maxlength :"limit of 24hrs",
            },
            is_headquater:{
                remote : "Headquater already exists"
            }
        },
        submitHandler: function(form) {
        form.submit();
        toastr.success('Location added successfully')

        }
    });
});

