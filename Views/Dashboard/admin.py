from flask import Blueprint,render_template,redirect,url_for,flash
from flask_login import login_required , current_user
from db import db
from Models_app import User, Link

admin_blp = Blueprint('admin',__name__)


@admin_blp.route('/admin',methods=['GET'])
@login_required
def dashboard():
    if current_user.is_admin == False:
        flash('You are not authorized to access this page!' , 'error')
        return redirect(url_for('dashboard.dashboard'))
    if current_user.is_admin == True:
        all_users = db.session.query(User).all()
        all_links = db.session.query(Link).all()
        return render_template('admin.html' , all_users=all_users , all_links=all_links , len=len)
    
    # return render_template('dashboard.html' ,links = user.links )

@admin_blp.route('/show_user/<id>')
@login_required
def show(id):
    if current_user.is_admin == False:
        flash('You are not authorized to access this page!' , 'error')
        return redirect(url_for('dashboard.dashboard'))
    user = db.session.query(User).get(id)
    return render_template('show_user.html' , user = user)

