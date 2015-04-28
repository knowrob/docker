# This file declares the Flask Singletons 'app' and 'db'
# 'app' and 'db' are defined in a separate file to avoid circular imports
# Usage: from app.app_and_db import app, db
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

# This is the WSGI compliant web application object
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)

# This is the SQLAlchemy ORM object
db = SQLAlchemy(app)

# Start openEASE webapps
from webrob.startup.init_webapps import init_webapps
init_webapps(app)
