# This file starts the WSGI web application.
# - Heroku starts gunicorn, which loads Procfile, which starts runserver.py
# - Developers can run it from the command line: python runserver.py

from webrob.app_and_db import app, db
from webrob.startup.init_app import init_app
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

init_app(app, db)

# Start a development web server if executed from the command line

if __name__ == '__main__':
    if 'DEBUG' in app.config and app.config['DEBUG']:
        app.run(host='0.0.0.0')
    else:
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(5000)
        IOLoop.instance().start()
