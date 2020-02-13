jQuery(document).ready(function() {  
    $("form[name='meeting']").validate({
    errorClass: "my-error-class", //for error colors
    // Specify validation rules
    rules: {
    // The key name on the left side is the name attribute
    // of an input field. Validation rules are defined
    // on the right side
    title: {
        required : true,
        remote : {url: "/test_meeting", async:false}
    },
    date_time: {
        required : true
    },
    time:{
        required : true
    },
    where: {
        required : true
    },
    attendees: {
        required : true
    },
    priority: {
        required : true
    },
    
        
    },
    // Specify validation error messages
    messages: {
        title:{
            required:"This field is required",
            remote : "Meeting with this name already exists.",
        } ,
        date_time: "This field is required",
        time :"This field is required",
        where: "This field is required",
        attendees: "This field is required",
        priority:"This field is required",
        
    },
    // Make sure the form is submitted to the destination defined
    // in the "action" attribute of the form when valid
    submitHandler: function(form) {
    form.submit();
    toastr.success('Meeting Created Successfully')
    }
})
});