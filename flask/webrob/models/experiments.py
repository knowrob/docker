
from webrob.app_and_db import db

class Project(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    url = db.Column(db.String(), nullable=False)

class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)

class Platform(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)

class Docu(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    key = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(), nullable=False)
