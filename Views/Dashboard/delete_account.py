from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask_login import login_required,current_user
from db import db
from Models_app import User,Link


delete_account_blp = Blueprint('delete_account_blp',__name__)


@delete_account_blp.route('/delete_account',methods=['GET','POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        user = db.session.query(User).filter_by(id=current_user.id).first()
        password = request.form.get('password')
        if user.check_password(password):
            for link in user.links:
                db.session.delete(link)
            db.session.delete(user)
            db.session.commit()
            flash('Your account has been deleted successfully' , 'success')
            return redirect(url_for('login.login_page'))
        else:
            flash('Wrong password' , 'error')
            return redirect(url_for('delete_account_blp.delete_account'))
    return render_template('delete_account.html')

@delete_account_blp.route('/delete_account/<id>',methods=['POST'])
@login_required
def delete_account_api(id):
    if current_user.is_admin == False:
        flash('You are not authorized to access this page!' , 'error')
        return redirect(url_for('dashboard.dashboard'))
    user = db.session.query(User).get(id)
    if user:
        for link in user.links:
            db.session.delete(link)
        db.session.delete(user)
        db.session.commit()
        flash('Account has been deleted successfully' , 'success')
        return redirect(url_for('admin.dashboard'))
    else:
        flash('User not found' , 'error')
        return redirect(url_for('admin.dashboard'))