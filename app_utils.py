from functools import wraps
from flask import current_app, redirect,request, render_template, make_response,session
import jwt
from datetime import datetime
import pytz
from os import getenv

# CONSTANTS for CURRENT APP
TZ = pytz.timezone('Asia/Kolkata')
MONGODB_ADMIN_PASSWORD = getenv("MONGODB_ADMIN_PASSWORD", default="password")
MONGODB_USER_PASSWORD = getenv("MONGODB_USER_PASSWORD", default="password")
MONGODB_ADMIN = getenv("MONGODB_ADMIN", default="admin")
MONGODB_USER = getenv("MONGODB_USER", default="test_user_1")

MONGODB_CLUSTER_URL = getenv("MONGODB_CLUSTER_URL", default="url")
MONGODB_URI_ADMIN = f"mongodb+srv://{MONGODB_ADMIN}:{MONGODB_ADMIN_PASSWORD}@{MONGODB_CLUSTER_URL}/?retryWrites=true&w=majority"
MONGODB_URI_USER = f"mongodb+srv://{MONGODB_USER}:{MONGODB_USER_PASSWORD}@{MONGODB_CLUSTER_URL}/?retryWrites=true&w=majority"

MONGODB_NAME = getenv("MONGODB_NAME", default="user-db")
MONGODB_COLLECTION_NAME = "links"


def token_required(func):
    '''
    Decorator to check if user logged in already or not to validate token.
    '''
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'] 
        elif 'token' in session:
            token = session['token']
        if not token:
            return render_template("failed.html", error = ("tokenMissing", "")), 401, {"message": "Missing Token."}
        
        current_user = None
        curr_perms = None
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data.get('userid')
            curr_perms = data.get('perms')
            exp = data.get("exp")
            iat = data.get("iat")
            if exp < round(datetime.now().timestamp()):
                return redirect('/auth/logout'), 401
        except:
            if 'user' in session:
                session.pop('user')
                if 'token' in session:       
                    session.pop('token')  
            return render_template("failed.html", error = ("invalidToken", "")), 401, {"message": "Invalid Token"}
        return func(username=current_user, perms=curr_perms)
    return decorator

