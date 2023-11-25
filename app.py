from flask import Flask,redirect,url_for,render_template,request,session
from db import db , login_manager , jwt

from datetime import timedelta

from Models_app import User, Link

import os
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db') #os.getenv('DATABASE')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

db.init_app(app)
login_manager.init_app(app)
jwt.init_app(app)


from Views.Dashboard.dashboard import dash_blp
from Views.Dashboard.add_link import add_link
from Views.Dashboard.edit import edit
from Views.Dashboard.delete import delete_blp
from Views.short_link import short_blp
from Views.login import log_blp
from Views.signup import sign_blp
from Views.Dashboard.confirm_reset.confirm_email import confirm_email_blp
from Views.Dashboard.confirm_reset.reset_password import password_reset_blp
from Views.Dashboard.delete_account import delete_account_blp
from Views.Dashboard.admin import admin_blp
app.register_blueprint(dash_blp,url_prefix="/portal")
app.register_blueprint(add_link,url_prefix="/portal")
app.register_blueprint(edit,url_prefix="/portal")
app.register_blueprint(delete_blp,url_prefix="/portal")
app.register_blueprint(log_blp,url_prefix="/portal")
app.register_blueprint(sign_blp,url_prefix="/portal")
app.register_blueprint(short_blp)
app.register_blueprint(confirm_email_blp,url_prefix="/portal")
app.register_blueprint(password_reset_blp,url_prefix="/portal")
app.register_blueprint(delete_account_blp,url_prefix="/portal")
app.register_blueprint(admin_blp,url_prefix="/portal")


@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')




@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=1)
    session.modified = True




if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)