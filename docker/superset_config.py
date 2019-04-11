import os
from flask_appbuilder.security.manager import AUTH_OID, AUTH_REMOTE_USER, AUTH_DB, AUTH_LDAP, AUTH_OAUTH
from werkzeug.contrib.cache import RedisCache

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = ['*']
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

# ---------------------------------------------------
# Auth
# ---------------------------------------------------
# AUTH_TYPE = AUTH_OAUTH
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Public"
PUBLIC_ROLE_LIKE_GAMMA = True
OAUTH_PROVIDERS = [
    {'name':'facebook', 'icon':'fa-facebook',
        'remote_app':{
            'base_url': 'https://graph.facebook.com/',
            'request_token_url': None,
            'access_token_url': '/oauth/access_token',
            'authorize_url': 'https://www.facebook.com/dialog/oauth',
            'consumer_key': 'FACEBOOK_AUTH_KEY',
            'consumer_secret': 'FACEBOOK_AUTH_SECRET',
            'request_token_params': {'scope': 'email'},
        }
    },
    {'name':'twitter', 'icon':'fa-twitter',
        'remote_app': {
            'consumer_key': 'TWITTER_AUTH_KEY',
            'consumer_secret': 'TWITTER_AUTH_SECRET',
            'base_url': 'https://api.twitter.com/1.1/',
            'request_token_url': 'https://api.twitter.com/oauth/request_token',
            'access_token_url': 'https://api.twitter.com/oauth/access_token',
            'authorize_url': 'https://api.twitter.com/oauth/authenticate'
        }
    },
    {'name': 'google', 'whitelist': ['@gmail.com'], 'icon': 'fa-google','token_key': 'access_token', 
       'remote_app': {
            'consumer_key': '459899766638-s1artlhp4osjeh4tot1dh013mi98noq9.apps.googleusercontent.com',
            'consumer_secret': 'knLnolnlTnLXRuUi73LJCVzm',
            'base_url': 'https://www.googleapis.com/oauth2/v2/',
            'request_token_params': {
            'scope': 'email profile'
            },
            'request_token_url': None,
            'access_token_url': 'https://accounts.google.com/o/oauth2/token',
            'authorize_url': 'https://accounts.google.com/o/oauth2/auth'
        }
    }
]

# ---------------------------------------------------
# Babel config for translations
# ---------------------------------------------------
# Setup default language
BABEL_DEFAULT_LOCALE = 'es'
# Your application default translation path
BABEL_DEFAULT_FOLDER = 'superset/translations'
# The allowed translation for you app
LANGUAGES = {
    'en': {'flag': 'us', 'name': 'English'},
    'es': {'flag': 'es', 'name': 'Español'}
}

# Cache de mapas
MAPBOX_API_KEY = os.environ.get('MAPBOX_API_KEY', 'pk.eyJ1IjoibGFmaWVicmVhbWFyaWxsYSIsImEiOiJjanUxbGE0MHIwMm8xNDRwcHI4eW45OGJmIn0.jBWrWYPRElevdncNn8dIsg')

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

## uploads
class CeleryConfig(object):
    BROKER_URL = 'redis://%s:%s/0' % (REDIS_HOST, REDIS_PORT)
    CELERY_IMPORTS = ('superset.sql_lab', )
    CELERY_RESULT_BACKEND = 'redis://%s:%s/1' % (REDIS_HOST, REDIS_PORT)
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
    CELERY_TASK_PROTOCOL = 1

CELERY_CONFIG = CeleryConfig