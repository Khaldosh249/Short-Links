from flask_smorest import Blueprint 
from flask import request
from flask_jwt_extended import create_access_token , get_jwt_identity , jwt_required
from db import db , jwt
from Models_app import User , Link


crud = Blueprint("crud" , __name__)


# Creat link
@crud.route("/link" , methods=["POST"])
@jwt_required()
def create_link():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    link_token = data.get("link_token")
    link_url = data.get("link_url")
    
    check_link = db.session.query(Link).with_entities(Link.token).filter_by(link_token=link_token).first()
    if check_link:
        return {"message": "Link already exists"} , 400
    
    link = Link(user_id=user_id , )
    db.session.add(link)
    db.session.commit()
    return link.to_dict()