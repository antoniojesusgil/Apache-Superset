# Configurar Superset

Cada configuración dependerá de las necesidades

## Mover ruta

Puede cambiarse la ruta y los directorios a otro punto de montaje del sistema, tan solo se ha de crear un enlace simbolico a las ruta original.

Movemos el directorio `/superset`a `/opt`

```
mv /usr/lib/python3.6/site-packages/superset /opt/
ln -s /opt/superset /usr/lib/python3.6/site-packages/superset 
```

# Configurar métodos AUTH

## OAUTH
```python
AUTH_TYPE = AUTH_OAUTH
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
```

# Babel 
```python
# Setup default language
BABEL_DEFAULT_LOCALE = 'en'
# Your application default translation path
BABEL_DEFAULT_FOLDER = 'superset/translations'
# The allowed translation for you app
LANGUAGES = {
    'en': {'flag': 'us', 'name': 'English'},
    'es': {'flag': 'es', 'name': 'Español'}
}
```
# Mapbox 
```python
# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY', 'pk.eyJ1IjoiY2NlcmNvcyIsImEiOiJjamNyeG4xZ2cyeDVzMnJueGh3cDk3bjc4In0.K7X-yR7rMJPzumJscjKRKQ')
```