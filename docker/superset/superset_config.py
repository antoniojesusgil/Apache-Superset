import os
from flask_appbuilder.security.manager import AUTH_OID, AUTH_REMOTE_USER, AUTH_DB, AUTH_LDAP, AUTH_OAUTH
from werkzeug.contrib.cache import RedisCache


def get_env_variable(var_name, default=None):
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = 'The environment variable {} was missing, abort...'\
                        .format(var_name)
            raise EnvironmentError(error_msg)

invocation_type = get_env_variable('INVOCATION_TYPE')
if invocation_type == 'COMPOSE':
    MYSQL_USER = get_env_variable('MYSQL_USER')
    MYSQL_PASS = get_env_variable('MYSQL_PASS')
    MYSQL_HOST = get_env_variable('MYSQL_HOST')
    MYSQL_PORT = get_env_variable('MYSQL_PORT')
    MYSQL_DATABASE = get_env_variable('MYSQL_DATABASE')

    # The SQLAlchemy connection string.
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER,
                                                           MYSQL_PASS,
                                                           MYSQL_HOST,
                                                           MYSQL_PORT,
                                                           MYSQL_DATABASE)
else:
    SQLALCHEMY_DATABASE_URI = get_env_variable('DB_URL')

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = ['*']
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

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
MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY', 'pk.eyJ1IjoibGFmaWVicmVhbWFyaWxsYSIsImEiOiJjanUxbGE0MHIwMm8xNDRwcHI4eW45OGJmIn0.jBWrWYPRElevdncNn8dIsg')

if invocation_type == 'COMPOSE':
    REDIS_HOST = get_env_variable('REDIS_HOST')
    REDIS_PORT = get_env_variable('REDIS_PORT')
else:
    REDIS_HOST = get_env_variable('REDIS_URL').split(":")[1].replace("/","")
    REDIS_PORT = get_env_variable('REDIS_URL').split(":")[2].replace("/0","")
RESULTS_BACKEND = RedisCache(host=REDIS_HOST, port=REDIS_PORT, key_prefix='superset_results')

class CeleryConfig(object):
    BROKER_URL = 'redis://%s:%s/0' % (REDIS_HOST, REDIS_PORT)
    CELERY_IMPORTS = ('superset.sql_lab', )
    CELERY_RESULT_BACKEND = 'redis://%s:%s/1' % (REDIS_HOST, REDIS_PORT)
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
    CELERY_TASK_PROTOCOL = 1


CELERY_CONFIG = CeleryConfig

SUPERSET_D3_LOCALE = """
{
  "decimal": ",",
  "thousands": ".",
  "grouping": [3],
  "currency": ["", "€"],
  "dateTime": "%a %b %e %X %Y",
  "date": "%d/%m/%Y",
  "time": "%H:%M:%S",
  "periods": ["AM", "PM"],
  "days": ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
  "shortDays": ["Dom", "Lun", "Mar", "Mi", "Jue", "Vie", "Sab"],
  "months": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
  "shortMonths": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
} """