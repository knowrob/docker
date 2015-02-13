import os

DEBUG=True
SECRET_KEY='\\\xf8\x12\xdc\xf5\xb2W\xd4Lh\xf5\x1a\xbf"\x05@Bg\xdf\xeb>E\xd8<'
#USERNAME='docker'
#PASSWORD='default'
SQLALCHEMY_DATABASE_URI = 'postgresql://docker@' + os.environ['POSTGRES_PORT_5432_TCP_ADDR'] + ':' + os.environ['POSTGRES_PORT_5432_TCP_PORT'] + '/docker'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'db/webrob.db')
#SQLALCHEMY_DATABASE_URI = 'postgresql://docker@localhost/db1/docker'

CSRF_ENABLED = True
#SERVER_NAME=''
MAIL_SERVER   = 'smtp.gmail.com'
MAIL_PORT     = 465
MAIL_USE_SSL  = True
MAIL_USERNAME = 'email@example.com'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = '"Sender" <noreply@example.com>'
USER_ENABLE_USERNAME = True
USER_ENABLE_EMAIL           = True
USER_ENABLE_CONFIRM_EMAIL = False

MESH_REPOSITORIES = [
    "http://svn.ai.uni-bremen.de/svn/cad_models/",
    "https://code.ros.org/svn/wg-ros-pkg/stacks/pr2_common/trunk/"
]


