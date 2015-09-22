import os

DEV_SECRET_KEY='\\\xf8\x12\xdc\xf5\xb2W\xd4Lh\xf5\x1a\xbf"\x05@Bg\xdf\xeb>E\xd8<'

SQLALCHEMY_DATABASE_URI = 'postgresql://docker@' + \
    os.environ['POSTGRES_PORT_5432_TCP_ADDR'] + ':' + \
    os.environ['POSTGRES_PORT_5432_TCP_PORT'] + '/docker'
#SQLALCHEMY_ECHO = True

CSRF_ENABLED = True

# email server
MAIL_SERVER   = os.environ.get('OPENEASE_MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT     = int(os.environ.get('OPENEASE_MAIL_PORT', '465'))
MAIL_USE_TLS  = bool(os.environ.get('OPENEASE_MAIL_USE_TLS', 'False'))
MAIL_USE_SSL  = bool(os.environ.get('OPENEASE_MAIL_USE_SSL', 'True'))
MAIL_USERNAME = os.environ.get('OPENEASE_MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('OPENEASE_MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = '"Sender" <openease.iai@gmail.com>'

USER_ENABLE_USERNAME = True
USER_ENABLE_EMAIL = True
USER_ENABLE_CONFIRM_EMAIL = False

MAX_HISTORY_LINES = 100

MESH_REPOSITORIES = [
    "http://svn.ai.uni-bremen.de/svn/cad_models/",
    "https://github.com/code-iai/iai_maps/raw/master/",
    "https://github.com/bbrieber/iai_robots/raw/master/",
    "https://github.com/PR2/pr2_common/raw/master/"
    #"https://github.com/code-iai/iai_robots/raw/master/",
    #"https://code.ros.org/svn/wg-ros-pkg/stacks/pr2_common/trunk/"
]
