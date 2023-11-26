from flask_smorest import Blueprint 
from flask import request
from flask_jwt_extended import create_access_token , get_jwt_identity , jwt_required
from db import db , jwt
from Models_app import User , Link


crud = Blueprint("crud" , __name__)


