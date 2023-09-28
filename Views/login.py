#from app import app
from db import db , login_manager

from Models_app import User, Link

from flask import Blueprint , request , url_for , redirect , render_template , flash
from flask_login import login_user , logout_user, login_required , current_user

log_blp = Blueprint('login' ,__name__)


@log_blp.route('/login' , methods = ["GET" , "POST"])
def login_page():

    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    elif request.method == "GET":
        #u = User("123@eltech.sd" , "123")
        #db.session.add(u)
        #db.session.commit()
        return render_template("login.html")
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        if len(email) == 0 or len(password) == 0:
            flash('Fill all fields' , 'info')
            return render_template('login.html')
        uu = db.session.query(User).filter_by(email=email).first()
        if uu:
            pass
        else:
            flash('Wrong email or password!' , 'error')
            return render_template("login.html")
        if uu.check_password(password):
            login_user(uu)
            """ if not uu.password_confirm:
                return redirect(url_for('reset_password.request_to_reset_password')) """
            if not uu.email_confirm:
                return redirect(url_for('confirm_email.confirm_email_page'))
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash('Wrong email or password!', 'error')
            return render_template("login.html")


@log_blp.route("/logout")
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('login.login_page'))