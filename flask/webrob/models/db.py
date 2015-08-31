
from flask_user import current_app
from webrob.app_and_db import app

import json

__author__ = 'danielb@cs.uni-bremen.de'

def db_columns(cls):
    return [{ 'name': c.name, 'type': c.type, 'nullable': c.nullable } for c in cls.__table__.columns]

def db_column_names(cls):
    return [c.name for c in cls.__table__.columns]

def db_find_all(cls):
    db_adapter = current_app.user_manager.db_adapter
    entries = db_adapter.find_all_objects(cls)
    columns = db_column_names(cls)
    out = []
    for e in entries:
        d = {}
        for m in columns: d[m] = e.__dict__[m]
        out.append(d)
    return out

def db_find(cls, i):
    db_adapter = current_app.user_manager.db_adapter
    return db_adapter.get_object(cls, i)

def db_update(cls, i, data):
    entry = db_find(cls,i)
    db_adapter = current_app.user_manager.db_adapter
    db_adapter.update_object(entry, **data)
    db_adapter.commit()

def db_create(cls, data):
    if 'id' in data: del data['id']
    db_adapter = current_app.user_manager.db_adapter
    db_adapter.add_object(cls, **data)
    db_adapter.commit()
    
def db_remove(cls, i):
    entry = db_find(cls,i)
    db_adapter = current_app.user_manager.db_adapter
    db_adapter.delete_object(entry)
    db_adapter.commit()

def db_table_class(table_name):
    db_adapter = current_app.user_manager.db_adapter
    for clazz in db_adapter.db.Model._decl_class_registry.values():
        try:
            if clazz.__tablename__==table_name: return clazz
        except:
            pass
    return None

    