jQuery(document).ready(function() {
    $("form[name='package']").validate({
        errorClass: 'my-error-class',
        rules: {
            name:{
                required : true,
                remote : {url: "/test_package", async:false}
            },
            description: 'required',
                    
        },
        messages: {
            name: {
                required : "This field is required",
                remote : "Package with this name is already registered.",
            },
            description: 'This field is required',
        
        },
        submitHandler: function(form) {
        form.submit();
        toastr.success('Package added successfully')

        }
    })
    $('#connectwise_check').on('click',function(){
        if( $(this).is(":checked")){
        $("#show").show()
        }
        else{
        $("#show").hide()
        }
    });
    $('#moneris_check').on('click',function(){
        if( $(this).is(":checked")){
        $("#show1").show()
        }
        else{
        $("#show1").hide()
        }
    });
});

