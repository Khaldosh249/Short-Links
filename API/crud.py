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
    
    
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        return {"message": "unvalid token"}  , 400
    
    check_link = db.session.query(Link).with_entities(Link.token).filter_by(token=link_token).first()
    if check_link:
        return {"message": "Link token already exists"} , 409
    
    
    link = Link(token=link_token , url=link_url ,user_id=user_id)
    db.session.add(link)
    db.session.commit()
    
    return link.to_dict() , 201


# Show URL
@crud.route("/link/<string:token>" , methods=["GET"])
@jwt_required()
def show_link(token):
    user_id = get_jwt_identity()
    
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        return {"message": "unvalid token"}  , 400
    
    link = db.session.query(Link).filter_by(token=token).first()
    if not link:
        return {"message": "Link not found"} , 404
    
    if link.user_id != user_id:
        return {"message": "unvalid token"} , 400
    
    return link.to_dict() , 200



#all links
@crud.route("/links" , methods=["GET"])
@jwt_required()
def show_all_links():
    user_id = get_jwt_identity()
    
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        return {"message": "unvalid token"}  , 400
    
    links = user.links
    
    return [link.to_dict() for link in links] , 200


#delete link
@crud.route("/link/<string:token>" , methods=["DELETE"])
@jwt_required()
def delete_link(token):
    user_id = get_jwt_identity()
    
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        return {"message": "unvalid token"}  , 400
    
    link = db.session.query(Link).filter_by(token=token).first()
    if not link:
        return {"message": "Link not found"} , 404
    
    if link.user_id != user_id:
        return {"message": "unvalid token"} , 400
    
    db.session.delete(link)
    db.session.commit()
    
    return {"message": "Link deleted"} , 200


#update link
@crud.route("/link/<string:token>" , methods=["PUT"])
@jwt_required()
def update_link(token):
    user_id = get_jwt_identity()
    
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        return {"message": "unvalid token"}  , 400
    
    link = db.session.query(Link).filter_by(token=token).first()
    if not link:
        return {"message": "Link not found"} , 404
    
    if link.user_id != user_id:
        return {"message": "unvalid token"} , 400
    
    data = request.get_json()
    link_token = data.get("link_token")
    link_url = data.get("link_url")
    
    link.token = link_token
    link.url = link_url
    db.session.add(link)
    db.session.commit()
    
    return link.to_dict() , 200