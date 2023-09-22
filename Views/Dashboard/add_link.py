from flask import Blueprint,render_template,request,redirect,url_for , flash
from flask_login import login_required,current_user
from Models_app import Link
from db import db

add_link = Blueprint('add',__name__)

@add_link.route('/add',methods=['GET' , 'POST'])
def link():
    if request.method == "GET":
        return render_template('add.html')
    else:
        url = request.form.get("long_url")
        if url[:4] != "http":
            url = "https://" + url
        token = request.form.get("token")
        if db.session.query(Link).filter_by(token=token).first():
            flash('Token already exists' , 'error')
            return render_template('add.html' , url=url , token=token)
        new_link = Link(token , url , current_user.id)
        db.session.add(new_link)
        db.session.commit()
        flash('Link added successfully' , 'success')
        return redirect(url_for('dashboard.dashboard'))