import os

# database
MONGODB_DB = 'postcards'
MONGODB_HOST = 'localhost'
MONGODB_PORT = '27017'

# email
SEND_MAIL = True
SMTP_SERVER = 'smtp.mailgun.org'
SMTP_LOGIN = 'postmaster@edinburghcollected.org'
SMTP_PASSWORD = ''
MAIL_SERVER = 'smtp.mailgun.org'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'postmaster@edinburghcollected.org'
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = 'postmaster@edinburghcollected.org'

# Admin user & pass
ADMIN_USER = 'admin'
ADMIN_PASSWORD = ''

# disable debugging in production
DEBUG = False