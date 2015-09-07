
from webrob.app_and_db import db

class Tutorial(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cat_id = db.Column(db.String(), nullable=False)
    cat_title = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(), nullable=False)
    page = db.Column(db.Integer(), nullable=False)

def read_tutorial_page(cat, page):
    return Tutorial.query.filter_by(cat_id=cat,page=page).first()
