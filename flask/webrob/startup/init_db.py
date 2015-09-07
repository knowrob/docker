
def init_db(app, db):
    # Automatically create all DB tables in app/app.sqlite file
    db.create_all()
    db.session.commit()
