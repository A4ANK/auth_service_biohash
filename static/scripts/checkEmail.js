$(document).ready(function(){
    $('#email').keyup( function(e){
        var email = $('#email').val();
        var regex = RegExp('[a-zA-Z0-9]+@[a-z]+\.[a-z]{2,3}');
        if(email != ''){
            if (regex.test(email)){
                $('#emailValidResponse').html("");
            }else{
                $('#emailValidResponse').html("* Email is not valid.").css({'color':'red', 'text-align':'left'});
                // "Email is not valid."
            }
        }
        if(email != '' && regex.test(email)){
            $.ajax({
                type: 'POST',
                url: '/checkemailonly',
                data: {email: email},
                success: function(response){
                    if (response.status == "Allowed"){
                    $('#emailResponse').html("");
                    $('#button').removeAttr('disabled');
                    }else{
                        $('#emailResponse').html("** "+response.status).css({'color':'red', 'text-align':'left'});
                        // "Email Already Taken."
                    }
                }
            });
        }else{
            $("#emailResponse").html("");
        }
    })
})