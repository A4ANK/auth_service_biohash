$(document).ready(function(){
    $('#username').keyup( function(e){
        var username = $('#username').val();
        if(username != ''){
            $.ajax({
                type: 'POST',
                url: '/checkuseronly',
                data: {username: username},
                success: function(response){
                    if (response.status == "Available"){
                    $('#usernameResponse').html(response.status).css({'color':'green', 'text-align':'left'});
                    $('#button').removeAttr('disabled');
                    }else{
                        $('#usernameResponse').html(response.status).css({'color':'red', 'text-align':'left'});
                        // "Username Already Taken."
                    }
                }
            });
        }else{
            $("#usernameResponse").html("");
        }
    })
})