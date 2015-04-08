from flask import session
from webrob.pages.utility import get_application_description

from prac.wordnet import WordNet
from webrob.app_and_db import app
from webrob.pracinit import prac

import os
    
def register_routes():
    from webrob.pages import log
    from webrob.pages import meshes
    from webrob.pages import views
    from webrob.pages import utils
    
    prac.wordnet = WordNet(concepts=None)
    app.config['ALLOWED_EXTENSIONS'] = set(['mln','db','pracmln'])