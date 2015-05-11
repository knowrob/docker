from pracWEB.pracinit import pracApp
import jinja2
import os

def register_routes():
    
    from webrob.app_and_db import app
    
    pracApp.app = app
    # use html templates from prac app
    prac_loader = jinja2.ChoiceLoader([
        pracApp.app.jinja_loader,
        jinja2.FileSystemLoader(['/opt/practools/tools/prac/pracGUI/pracWEB/templates']),
    ])
    pracApp.app.jinja_loader = prac_loader
    pracApp.app.config['PRAC_STATIC_PATH'] = '/opt/practools/tools/prac/pracGUI/pracWEB/build'

    pracApp.app.secret_key = 'so secret!'


    from webrob.pages import log
    from pracWEB.pages import inference
    from pracWEB.pages import views
    from pracWEB.pages import utils
