from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()

login_manager.login_view = 'login.login_page'

login_manager.refresh_view = 'login.login_page'
login_manager.needs_refresh_message = (u"Session timedout, please re-login")
login_manager.needs_refresh_message_category = "error"
