import os

DEV_SECRET_KEY='\\\xf8\x12\xdc\xf5\xb2W\xd4Lh\xf5\x1a\xbf"\x05@Bg\xdf\xeb>E\xd8<'

SQLALCHEMY_DATABASE_URI = 'postgresql://docker@' + \
    os.environ['POSTGRES_PORT_5432_TCP_ADDR'] + ':' + \
    os.environ['POSTGRES_PORT_5432_TCP_PORT'] + '/docker'

CSRF_ENABLED = True

# TODO: Support for mail service
MAIL_SERVER   = 'smtp.gmail.com'
MAIL_PORT     = 465
MAIL_USE_SSL  = True
MAIL_USERNAME = 'email@example.com'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = '"Sender" <noreply@example.com>'
USER_ENABLE_USERNAME = True
USER_ENABLE_EMAIL           = True
USER_ENABLE_CONFIRM_EMAIL = False