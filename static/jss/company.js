jQuery(document).ready(function() {
    $('form[id="form9"]').validate({
        errorClass: 'my-error-class',
        rules: {
            company_name: {
                required : true,
                remote : {url: "/test_company", async:false}
            },
            contact_number: {
                required : true,
                maxlength : 10,
            },
            description: 'required',
            company_website: {
                required : true,
            },
            company_logo: {
                extension: "jpg|jpeg|png|ico|bmp"
            },
            company_address: {
                required : true,
                maxlength : 100,
            },
            company_location: {
                required : true,
                maxlength : 20,
            },
            company_pincode: {
                required : true,
                maxlength : 6,
            }
        },
        messages: {
            company_name: {
                required : "This field is required",
                remote : "Company with this name is already registered.",
            },
            contact_number :{
                required : "this field is required",
                maxlength : "only 10 digit number is allowed"
            },
            description: 'This field is required',
            company_website: 'This field is required',
            company_logo: {
            extension:'Please upload file in these format only (jpg, jpeg, png, ico, bmp).'
            },
            company_address: {
                required : 'This field is required',
                maxlength : 'only 100 characters are allowed'
            },
            company_location: {
                required : 'This field is required',
                maxlength : 'only 20 characters are allowed'
            },
            company_pincode: {
                required: "This field is required",
                maxlength: "Pincode can only contains 6 digits"
              },
            
            
        },
        submitHandler: function(form) {
        form.submit();
        toastr.success('Company added successfully')

        }
    });
});

