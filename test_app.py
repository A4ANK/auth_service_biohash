from flask import Flask, make_response, render_template, request
from app_utils  import token_required
from app import app as auth_app
from bio_auth.check_credentials import checkBioImage

@auth_app.route('/test_server', methods = ['GET', 'POST'])
@token_required
def test_server(*args, **kwargs): # kwargs => username = None 
    '''
    Home Page of Test App server which requires Authorization.
    '''
    if(request.method == 'POST'): 
        imageFile = request.files['image'] 
        accept = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
        
        if( imageFile is not None and
            imageFile.filename.rsplit('.', 1)[1].lower() in accept
            ):
            username = kwargs['username']
            bioImage = imageFile.read()
            imageFile.close()
            if(checkBioImage(username, bioImage)):
                return render_template("test_server.html", username = username), 401
            else:
                return make_response(
                '''
                Bio Hash is not verified. 
                <a href="/test_server"><button >Try Again</button></a>
                ''', 
                401
                )
    return render_template("test_form.html"), 200 # GET

if __name__ == '__main__':
    pass