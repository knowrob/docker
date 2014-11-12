
from webrob.app_and_db import db

class TutorialPage(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cat_id = db.Column(db.Integer(), nullable=False)
    cat_title = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(), nullable=False)
