import datetime
from flask import current_app
from webrob.models.users import User
from webrob.models.tutorials import Tutorial

def init_db(app, db):

    db.create_all()
    db.reflect(app=app)
    engine = db.get_engine(app)
    meta = db.metadata
    meta.reflect(bind=engine)
    
    db.session.commit()
