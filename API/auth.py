from flask_smorest import Blueprint 
from flask import request
from flask_jwt_extended import create_access_token , get_jwt_identity , jwt_required
from db import db , jwt
from Models_app import User , Link


auth = Blueprint("auth" , __name__)


@auth.route("/login")
def login():
    
    body = request.get_json()
    
    username = body.get("username")
    password = body.get("password")
    
    user = db.session.query(User).filter_by(email=username).first()
    if user and user.check_password(password):
        token = create_access_token(identity=username)
        return {"access_token": token}
    else:
        return {"message": "Invalid username or password"}, 401