from configparser import ConfigParser

parser = ConfigParser()
parser.read('settings.ini')

class Config():
    SECRET_KEY = parser.get('settings', 'SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = parser.get('sql', 'SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = parser.get('email', 'email')
    MAIL_PASSWORD = parser.get('email', 'password')

def GetChangelog():
    with open('changelog.txt') as f:
        log = f.read()
    return log
