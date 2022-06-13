from functools import wraps
import socket
import os
import jwt
from flask import Flask, render_template, request, redirect, session, make_response, jsonify, abort
from bio_auth.reg_db import createDB
from bio_auth.reg_biohash import sendCredentialToStore
from bio_auth.reg_server import registerServerInStore
from bio_auth.check_credentials import checkBioImage, checkUserRegisterInDB, checkUseronly
from bio_auth.update_credentials import updateUserCredentials


app = Flask(__name__, template_folder='templates', static_url_path='/static')


port = os.getenv("PORT", 8080)
app.config['SECRET_KEY'] = app.secret_key = os.getenv('SECRET_KEY') or 'keyforsigningCookie'


def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'] 
        elif 'token' in session:
            token = session['token']
        if not token:
            return render_template("failed.html", error = ("tokenMissing", "")), 401, {"message": "Missing Token."}
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['userid']
        except:
            return make_response(jsonify({"message": "Invalid Token"}), 401)
        return func(current_user, *args, **kwargs)
    return decorator


@app.route('/')
def index():
    return render_template('index.html'), 200

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/auth/login', methods = ['POST', 'GET'])
def login():
    if request.headers.get('authorization') is not None:
        username = request.authorization.username
        password = request.authorization.password
        if checkUserRegisterInDB(username, password):
            token = jwt.encode({'userid': username}, app.config['SECRET_KEY'], 'HS256')
            session['user'] = username
            session['token'] = token
            return render_template('dashboard.html', username=session['user'],), 201, {'Authorization': 'Bearer {}'.format(token)}
        return render_template("wrong.html"), 401, {'WWW-Authenticate': 'Basic-realm= "Login Required."'}
    
    elif(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')    

        if checkUserRegisterInDB(username, password):
            token = jwt.encode({'userid': username}, app.config['SECRET_KEY'], 'HS256')
            session['user'] = username
            session['token'] = token
            return render_template('dashboard.html', username=session['user'],), 201, {'Authorization': 'Bearer {}'.format(token)}
        return render_template("wrong.html"), 401, {'WWW-Authenticate': 'Basic-realm= "Login Required."'}

    return render_template("login.html")


@app.route('/auth/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    elif('user' in session and session['user'] == request.form.get('username')):
        return redirect('/dashboard')
    elif(request.method == 'POST'):
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')   
        imageFile = request.files['image'] 
        accept = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
        
        if(checkUseronly(username)):
            return render_template('failed.html', error = ("userExists", username)), 400

        elif( imageFile is not None and
            imageFile.filename.rsplit('.', 1)[1].lower() in accept
            ):
            token = jwt.encode({'userid': username}, app.config['SECRET_KEY'], 'HS256')
            session['user'] = username
            session['token'] = token
            userid = username
            passwd = password
            email = email
            bioImage = imageFile.read()
            imageFile.close()
            sendCredentialToStore(userid, passwd, email, bioImage)
            
            return render_template("success.html", success = ('registerSuccess', username)), 202

        return redirect('/errors/signup'), 415
    else:
        return render_template("signup.html")


@app.route('/auth/forgot', methods = ['POST', 'GET'])
def forgot():
    if request.method == 'GET':
        return render_template("forgot.html")
    elif(request.method == 'POST'):
        username = request.form.get('username')
        newPassword = request.form.get('password')   
        imageFile = request.files['image'] 
        accept = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
        if( checkUseronly(username) and
            imageFile is not None and
            imageFile.filename.rsplit('.', 1)[1].lower() in accept
        ):
            bioImage = imageFile.read()
            imageFile.close()
            if (checkBioImage(username, bioImage)):
                if(updateUserCredentials(username, newPassword)):
                    return render_template("success.html", success = ('forgotSuccess', username)), 202
                else:
                    print(f"Error in forgot password.")
                    return render_template("failed.html", error = ("forgotError", username)), 400

        return render_template("failed.html", error = ("forgotError", username)), 400
    else:
        return render_template("failed.html", error = ("forgotError", username)), 400

@app.route('/dashboard')
@app.route('/dashboard/<username>')
@token_required
def dashboard(username = None):
    if('user' in session and checkUseronly(session['user'])):
        return render_template("dashboard.html", username=session['user'],), 201
    
    return render_template("failed.html", error = ("NotLoggedIn", "")), 401, {'WWW-Authenticate': 'Basic-realm= "Login required!"'} 

@app.route('/auth/logout')
@token_required
def logout(username = None):
    if 'user' in session and checkUseronly(session['user']):
        username = session['user']
        session.pop('user')
        session.pop('token')          
        return render_template('logout.html', username = username), 200
    else:
        print("User not logged out successfully.")
        return render_template("failed.html", error = ("NotLoggedOut", "")), 401


@app.errorhandler(404)
def pageNotFoundError(error):
    return render_template('404.html', error = error), 404

@app.errorhandler(500)
def internalServerError(error):
    return render_template('500.html', error = error), 500


@app.route('/success')
def success():
    return render_template('success.html'), 202

@app.route('/failure')
def failure():
    return render_template('failed.html'), 400

@app.route('/errors/<error>')
def error(error = None):
    app.logger.info('Initialize error list.')
    errors = {
        "error": "Internal Server Error",
        "login": "Login Error",
        "logout": "Logout Error",
        "signup": f"Error in entered Email / Username / Password / Uploaded Image File. Supported Image File Extensions [jpg, png, jpeg, gif, bmp]"
    }
    try:
        app.logger.debug(f'Get message with error Key: {error}')
        if error not in errors.keys():
            return abort(404)
        elif 'login' == error:
            return render_template('error.html', error=errors['login'])
        elif 'logout' == error:
            return render_template('error.html', error=errors['logout'])
        elif 'signup' == error:
            return render_template('error.html', error=errors['signup'])
        elif 'error' == error:
            abort(500)   
    except KeyError:
        app.logger.error(f'Key {error} is causing an KeyError')
        abort(404)


if __name__ == '__main__':
    createDB()
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    serverID = hostname + "-" + ip

    registerServerInStore(serverID)

    # app.run(port=port, debug=True, ssl_context=('pki/server.crt', 'pki/server.key'))
    app.run(port=port, debug=True)