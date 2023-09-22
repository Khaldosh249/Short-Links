from flask import Blueprint , request , url_for , redirect , render_template , flash
from Models_app import Link
from db import db

short_blp = Blueprint('short' ,__name__)


@short_blp.route('/<token>' , methods = ["GET"])
def short_link(token):
    link = db.session.query(Link).filter_by(token=token).first()
    if link:
        link.visited()
        db.session.commit()
        return redirect(link.url)
    else:
        return render_template("404.html")