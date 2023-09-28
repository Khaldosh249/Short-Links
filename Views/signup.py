from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from Models_app import User
from db import db

sign_blp = Blueprint('sign', __name__)

@sign_blp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        if len(email) == 0 or len(password) == 0 or len(name) == 0:
            flash('Fill all fields' , 'info')
            return render_template('signup.html')
        if db.session.query(User).filter_by(email=email).first():
            flash('Email already exists' , 'info')
            return redirect(url_for('sign.signup'))
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        try:
            logout_user()
        except:
            pass
        flash('Account created successfully' , 'success')
        return redirect(url_for('login.login_page'))