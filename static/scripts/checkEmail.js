$(document).ready(function(){
    $('#email').keyup( function(e){
        var email = $('#email').val();
        if(email != ''){
            $.ajax({
                type: 'POST',
                url: '/checkemailonly',
                data: {email: email},
                success: function(response){
                    if (response.status == "Allowed"){
                    $('#emailResponse').html("");
                    $('#button').removeAttr('disabled');
                    }else{
                        $('#emailResponse').html(response.status).css({'color':'red', 'text-align':'left'});
                        // "Email Already Taken."
                    }
                }
            });
        }else{
            $("#emailResponse").html("");
        }
    })
})