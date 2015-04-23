from pracFlaskApp.pracinit import pracApp
import jinja2
import os

def register_routes():
    
    from webrob.app_and_db import app
    
    pracApp.app = app
    # use html templates from prac app
    prac_loader = jinja2.ChoiceLoader([
        pracApp.app.jinja_loader,
        jinja2.FileSystemLoader(['/opt/practools/tools/prac/pracGUI/pracFlaskApp/templates']),
    ])
    pracApp.app.jinja_loader = prac_loader
    pracApp.app.config['PRAC_STATIC_PATH'] = '/opt/practools/tools/prac/pracGUI/pracFlaskApp/static'

    from webrob.pages import log
    from pracFlaskApp.pages import views
    from pracFlaskApp.pages import utils
