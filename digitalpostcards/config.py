import os

# database
MONGODB_DB = 'postcards'
MONGODB_HOST = os.environ.get('DB_PORT_27017_TCP_ADDR')
MONGODB_PORT = os.environ.get('DB_PORT_27017_TCP_PORT')

# email
SEND_MAIL = False
MAIL_SERVER = 'localhost'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ''

# Admin user & pass
ADMIN_USER = 'admin'
ADMIN_PASSWORD = 'pass'

# disable debugging in production
DEBUG = True
