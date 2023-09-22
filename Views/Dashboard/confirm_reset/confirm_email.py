from db import db , login_manager

from Models_app import User
from Email_Send import send_email_verify

from flask import Blueprint , request , url_for , redirect , render_template , flash
from flask_login import login_user , logout_user, login_required , current_user

from URL_token_confirm_reset import confirm_email_token , generate_email_token

confirm_email_blp = Blueprint('confirm_email' ,__name__)





@confirm_email_blp.route("/email-verification/<token>")
def confirm_email(token):
    email = confirm_email_token(token)
    if email == False:
        flash("The confirmation link is invalid or has expired.", "error")
        return redirect(url_for("login.login_page"))
    user = db.session.query(User).filter_by(email=email).first() #User.query.filter_by(email=current_user.email).first_or_404()
    user.email_confirm = True
    db.session.add(user)
    db.session.commit()
    flash("You have confirmed your account. Thanks!", "success")
    return redirect(url_for("login.login_page"))


@confirm_email_blp.route('/email-verification' , methods = ["GET"])
@login_required
def confirm_email_page():
    if current_user.email_confirm:
        flash("Account already confirmed.", "success")
        return redirect(url_for("login.login_page"))
    
    if request.method == "GET":
        send_email_verify(current_user.email , url_for('confirm_email.confirm_email' , token=generate_email_token(current_user.email) , _external=True))
        flash("A new confirmation email has been sent. confirm your email first then login.", "success")
        logout_user()
        return redirect(url_for('login.login_page'))
    return redirect(url_for('login.login_page'))

