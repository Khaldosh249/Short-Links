from flask import Blueprint,render_template,request,redirect,url_for , flash
from flask_login import login_required,current_user
from Models_app import Link
from db import db

delete_blp = Blueprint('delete',__name__)

@delete_blp.route('/delete/<token>',methods=['POST'])
@login_required
def link(token):
    link = db.session.query(Link).filter_by(token=token).first()
    if link.user_id == current_user.id:
        db.session.delete(link)
        db.session.commit()
        flash('Link deleted successfully' , 'success')
        return redirect(url_for('dashboard.dashboard'))
    else:
        flash('You are not authorized to delete this link' , 'error')
        return redirect(url_for('dashboard.dashboard'))