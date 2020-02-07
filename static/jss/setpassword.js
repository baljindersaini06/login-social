jQuery(document).ready(function() {   
    $("form[name='setpassword']").validate({
    errorClass: "my-error-class", //for error colors
    // Specify validation rules
    rules: {
    // The key name on the left side is the name attribute
    // of an input field. Validation rules are defined
    // on the right side
        password: {
            required : true,
            minlength : 8
        },
        confirm_password: {
            required : true,
            equalTo: "#password"
        }
    },
    // Specify validation error messages
    messages: {
        password: {
            required:"This field is required",
            minlength:"password must contain atleast 8 characters with atleast one number. "
        },
        confirm_password: {
            required:"This field is required",
            equalTo:"Enter the same password as above."
        }
       
    },
    // Make sure the form is submitted to the destination defined
    // in the "action" attribute of the form when valid
    submitHandler: function(form) {
    form.submit();
    toastr.success('Password set Successfully')
    }
})

});