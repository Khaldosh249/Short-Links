from db import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash , check_password_hash

from flask import url_for

import os
from dotenv import load_dotenv
load_dotenv()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,user_id) #AdminUser.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100) , unique=True)
    password_hash = db.Column(db.String(500))
    email_confirm = db.Column(db.Boolean , default=False)
    password_reset = db.Column(db.Boolean , default=False)
    is_admin = db.Column(db.Boolean)
    links = db.relationship('Link' , backref='user' , lazy=True)
    
    
    def __init__(self , name:str , email:str , password:str ):
        """Initail new User
        
        Keyword arguments:
        name -- User name \n
        email -- User Email \n
        password -- User password \n
        Return: Null , Initail
        """
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        if email[-10:] == '@eltech.sd' or email in eval(os.getenv('ADMIN_EMAILS')):
            self.is_admin = True
        else:
            self.is_admin = False
    
    def check_password(self, password:str) -> bool:
        """Check for password to Log in"""
        return check_password_hash(self.password_hash , password)
    
    
    def change_password(self , password):
        self.password_hash = generate_password_hash(password)


class Link(db.Model):
    __tablename__ = 'links'
    
    id = db.Column(db.Integer , primary_key=True)
    token = db.Column(db.String(100) , unique=True)
    url = db.Column(db.String(100))
    visits = db.Column(db.Integer , default=0)
    user_id = db.Column(db.Integer , db.ForeignKey('users.id'))
    
    def __init__(self , token , url , user_id):
        self.token = token
        self.url = url
        self.user_id = user_id
    
    def visited(self):
        self.visits +=1
        return True
    
    def to_dict(self):
        return {
            'id':self.id,
            'token':self.token,
            'short_url' :url_for('short.short_link' , token=self.token , _external=True),
            'url':self.url,
            'visits':self.visits
            }

