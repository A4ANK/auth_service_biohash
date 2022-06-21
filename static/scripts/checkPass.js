$(document).ready(function(){
    $('#repeatPassword').keyup( function(e){
        var password = $('#password').val(); 
        var repeatPassword = $('#repeatPassword').val();
        if(password != repeatPassword){
           $('#passResponse').html("Passwords entered do not match.").css({'color':'red', 'text-align':'left'});
           $('#button').prop('disabled', true);
        }
        else{ 
           $("#passResponse").html(""); 
           $('#button').removeAttr('disabled'); 
        }
    })
})