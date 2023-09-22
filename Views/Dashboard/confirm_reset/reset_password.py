#from app import app
from db import db , login_manager

from Models_app import User

from Email_Send import send_reset_password

from flask import Blueprint , request , url_for , redirect , render_template , flash
from flask_login import login_user , logout_user, login_required , current_user

from URL_token_confirm_reset import confirm_password_token , generate_password_token


password_reset_blp = Blueprint('reset_password' ,__name__)




@password_reset_blp.route('/reset-password' , methods = ["GET" , "POST"])
def request_to_reset_password():
    if request.method == "GET":
        return render_template('forgetpass.html')
    else:
        email = request.form.get('email')
        user = db.session.query(User).filter_by(email=email).first()
        if user is not None:
            link = url_for('reset_password.password_reset' , token =generate_password_token(user.email) , _external=True)
            send_reset_password(user.email , link)
            user.password_reset = True
            db.session.add(user)
            db.session.commit()
            flash('Email sent!' , 'success')
            return redirect(url_for('login.login_page'))
        else:
            flash("Email not found!", 'error')
            return render_template("forgetpass.html")


@password_reset_blp.route('/reset-password/<token>' , methods = ["GET" , "POST"])
def password_reset(token):
    if request.method == "GET":
        confirm = confirm_password_token(token)
        if confirm == False:
            flash("The link is invalid or has expired." , 'error')
            return redirect(url_for('login.login_page'))
        try:
            user = db.session.query(User).filter_by(email=confirm).first()
            if not user.password_reset:
                flash("The link is invalid or has expired." , 'error')
                return redirect(url_for('login.login_page'))
        except:
            pass
        return render_template('resetpass.html')
    else:
        confirm = confirm_password_token(token)
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        if confirm == False:
            flash("The link is invalid or has expired." , 'error')
            return redirect(url_for('login.login_page'))
        if password != repassword:
            flash('Password must match' , 'error')
            return render_template('resetpass.html')
        user = db.session.query(User).filter_by(email=confirm).first()
        if password == repassword and user.password_reset:
            user.change_password(password)
            user.password_reset = False
            db.session.add(user)
            db.session.commit()
            flash('Password changed!' , 'success')
            return redirect(url_for('login.login_page'))
        else:
            return redirect(url_for('login.login_page'))


