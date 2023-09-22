from flask import Blueprint,render_template,request,redirect,url_for , flash
from flask_login import login_required,current_user
from Models_app import Link
from db import db

edit = Blueprint('edit',__name__)

@edit.route('/edit/<token>',methods=['GET' , 'POST'])
@login_required
def link(token):
    if request.method == "GET":
        link = db.session.query(Link).filter_by(token=token).first()
        if link.user_id == current_user.id:
            return render_template('edit.html' , link=link)
        else:
            flash('You are not authorized to edit this link' , 'error')
            return redirect(url_for('dashboard.dashboard'))
    else:
        url = request.form.get("long_url")
        tok = request.form.get("token")
        if url[:4] != "http":
            url = "https://" + url
        link = db.session.query(Link).filter_by(token=token).first()
        if link.user_id == current_user.id:
            link.url = url
            link.token = tok
            db.session.commit()
            flash('Link edited successfully' , 'success')
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('You are not authorized to edit this link' , 'error')
            return redirect(url_for('dashboard.dashboard'))