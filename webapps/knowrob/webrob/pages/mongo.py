
from flask import session, render_template, stream_with_context, Response
from flask_user import login_required

import os
from time import time, sleep
from subprocess import call

from webrob.pages.experiments import get_experiment_list, get_experiment_path
from webrob.pages.utility import admin_required
from webrob.app_and_db import app

from pymongo import MongoClient

def mongoDBName(category, experiment):
    return category+"_"+experiment

def mongoConnect():
    host = os.environ['MONGO_PORT_27017_TCP_ADDR']
    port = os.environ['MONGO_PORT_27017_TCP_PORT']
    return MongoClient(host, int(port))

@app.route('/knowrob/admin/mongo')
@admin_required
def admin_mongo():
    mng = mongoConnect()
    
    db_info = {}
    file_info = {}
    
    for (cat,exp) in get_experiment_list():
        db_name = mongoDBName(cat,exp)
        
        # Mongo stats
        stats =  mng[db_name].command("dbStats")
        db_info[db_name] = {
            'size': round((stats['dataSize'])/(1024.0*1024.0), 2),
            'avgObjSize': round((stats['avgObjSize'])/(1024.0*1024.0), 2),
            'objects': stats['objects'],
            'collections': stats['collections']
        }
        
        size = 0
        collections = set()
        for (collection,f) in get_episode_files(cat,exp):
            size += round((os.path.getsize(f))/(1024.0*1024.0), 2)
            collections.add(collection)
            
        file_info[db_name] = {
            'category': cat,
            'experiment': exp,
            'episodes': get_episode_count(cat,exp),
            'size': size,
            'collections': list(collections)
        }
    
    mng.close()
    return render_template('admin_mongo.html', **locals())

@app.route('/knowrob/admin/mongo_update/<cat>/<exp>', methods=['GET', 'POST'])
@admin_required
def admin_mongo_update(cat,exp):
    db_name = mongoDBName(cat,exp)
    # Drop old DB content
    mng = mongoConnect()
    mng.drop_database(db_name)
    mng.close()
    # Import all JSON/BSON files in episode directories
    def mng_import():
        collections = set()
        for (collection,data_file) in get_episode_files(cat,exp):
            app.logger.info("Importing " + data_file)
            collections.add(collection)
            if data_file.endswith('.json'):
                mng_import_json(db_name, collection, data_file)
            if data_file.endswith('.bson'):
                mng_import_bson(db_name, collection, data_file)
            yield 'Imported %s.\n' % (data_file)
        
        # Create indices
        mng = mongoConnect()
        db = mng[db_name]
        for collection_name in list(collections):
            db[collection_name].ensure_index('__recorded')
            yield 'Search index created for %s.__recorded.\n' % (collection_name)
            if collection_name == 'tf':
                db[collection_name].ensure_index('transforms.header.stamp')
                yield 'Search index created for %s.transforms.header.stamp.\n' % (collection_name)
        mng.close()
        
    return Response(stream_with_context(mng_import()))

def get_episode_count(cat,exp):
    exp_path = get_experiment_path(cat,exp)
    count = 0
    for episode in os.listdir(exp_path):
        episode_dir = os.path.join(exp_path, episode)
        if not os.path.isdir(episode_dir): continue
        count += 1
    return count

def get_episode_files(cat,exp):
    episode_files = []
    exp_path = get_experiment_path(cat,exp)
    for episode in os.listdir(exp_path):
        episode_dir = os.path.join(exp_path, episode)
        if not os.path.isdir(episode_dir): continue
        for f in os.listdir(episode_dir):
            if f.endswith('.json') or f.endswith('.bson'):
                episode_files.append((f[:-5], os.path.join(episode_dir,f)))
    return episode_files

def mng_import_json(db_name, collection, json_file):
    call(["mongoimport",
          "--host", os.environ['MONGO_PORT_27017_TCP_ADDR'],
          "--port", os.environ['MONGO_PORT_27017_TCP_PORT'],
          "--db", db_name,
          "--collection", collection,
          "--file", str(json_file)
    ])

def mng_import_bson(db_name, collection, bson_file):
    call(["mongorestore",
          "--host", os.environ['MONGO_PORT_27017_TCP_ADDR'],
          "--port", os.environ['MONGO_PORT_27017_TCP_PORT'],
          "--db", db_name,
          "--collection", collection,
          str(bson_file)
    ])
    
    
