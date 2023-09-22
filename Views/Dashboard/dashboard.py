from flask import Blueprint,render_template
from flask_login import login_required , current_user
from db import db
from Models_app import User, Link

dash_blp = Blueprint('dashboard',__name__)


@dash_blp.route('/dashboard',methods=['GET'])
@login_required
def dashboard():
    user = db.session.query(User).get(current_user.id)
    return render_template('dashboard.html' ,links = user.links )