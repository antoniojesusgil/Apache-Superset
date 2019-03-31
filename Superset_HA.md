# Superset Arquitectura HA

Objetivo:

Construir un sistema escalable, distribuido con alta disponibilidad y caché.

Componentes:

* Superset
* Nginx
* Gunicorn
* Redis
* Celery

![supersetHA_arquitectura](/uploads/de8392b6dec1d89ab530e99ccf4e0261/supersetHA_arquitectura.PNG)


## Superset 

[Versión inicial 0.26.3](http://asidvizint.asepeyo.site/static/assets/version_info.json) 
[Actualizada a versión 0.27](http://asidvizint.asepeyo.site/static/assets/version_info.json) 

## Nginx

Hace la función de proxy entre las peticiones cliente y el back-end.

Editar el archivo `nginx.conf` y modificar la sección `server` dentro de `http`

```bash
 server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  /var/log/nginx/host.access.log  main;

        location / {
            #root   /srv/www/htdocs/;
            #index  index.html index.htm;
            proxy_pass http://localhost:8000/;
        }
```


## Gunicorn 

Es un Web [Server Gateway Interface HTTP](http://docs.gunicorn.org/en/stable/index.html), sirve contenido mediante la administración de múltiples peticiones simultáneas.


### Instalación

`$ pip install gunicorn`

#### Workers

Son procesos instanciados de Gunicorn encargados de recibir la petición http, procesarla y devolverla.

#### Cálculo de los Workers

En función de la cantidad de CPU's disponibles en el sistema. Normalmente se utiliza la fórmula `n * 2 + 1`

Ejemplo para un sistema con 2 CPU's
```
(2 * 2) + 1 = 5
```

## Redis server

La función principal de Redis en esta aquitectura es la de disponer un sistema de caché back-end.

#### Redis como cache

* [web config. oficial](https://redis.io/topics/config)
* [algoritmo utilizado](https://redis.io/topics/lru-cache)

### Instalar redis
```sh
asidvizint:/usr/lib/python3.6 # https_proxy=https://xxx.costaisa.org:9090
asidvizint:/usr/lib/python3.6 # pip install redis
Collecting redis
  Downloading https://files.pythonhosted.org/packages/3b/f6/7a76333cf0b9251ecf49efff635015171843d9b977e4ffcf59f9c4428052/redis-2.10.6-py2.py3-none-any.whl (64kB)
    100% |████████████████████████████████| 71kB 2.3MB/s
Installing collected packages: redis
Successfully installed redis-2.10.6
```

## Celery

Distributed Task Query, [Celery](http://www.celeryproject.org/) es una cola de tareas asíncrona basada en el paso de mensajes distribuidos basados en tiempo real.  

Al utilizar un sistema de caché, Celery ofrece respuestas más rápidas comparadas con un sistema tradicional de llamadas a backend.

* [Celery & Brokers](http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html)

* [Using Redis](http://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html)

* [Celery & Redis como cola de mensajes](http://docs.celeryproject.org/en/v2.3.3/tutorials/otherqueues.html)


# Configurar front y gateway back

La primera aproximación es establecer la comunicación entre las capas frontend y backend.

### Nginx 

Partimos de nginx configurado como proxy pass apuntando a la dirección y puerto que previamente hemos establecido para el servicio.

### Gunicorn

Servir gunicorn con los parámetros: `--workers` Número de procesos a ejecutar, `--timeout` En segundos `--bind` Socket de servicio a enlazar.  

```bash
superset@asidvizint:~> gunicorn -w 5 --timeout 120 -b 0.0.0.0:8000 superset:app
[2018-08-22 11:52:33 +0200] [27026] [INFO] Starting gunicorn 19.9.0
[2018-08-22 11:52:33 +0200] [27026] [INFO] Listening at: http://0.0.0.0:8000 (27026)
[2018-08-22 11:52:33 +0200] [27026] [INFO] Using worker: sync
[2018-08-22 11:52:33 +0200] [27029] [INFO] Booting worker with pid: 27029
[2018-08-22 11:52:33 +0200] [27030] [INFO] Booting worker with pid: 27030
[2018-08-22 11:52:33 +0200] [27032] [INFO] Booting worker with pid: 27032
[2018-08-22 11:52:33 +0200] [27033] [INFO] Booting worker with pid: 27033
[2018-08-22 11:52:33 +0200] [27036] [INFO] Booting worker with pid: 27036
```
### Comprobar que responden los sistemas

``` 
http://http://asidvizint.asepeyo.site/
```
![asidvizint.asepeyo.site](/uploads/99a08bb9d41f03bcbd3123bf68ee1429/asidvizint.asepeyo.site.png)


# Configurar Redis como caché

Para disponer un sistema de caché con Redis se han añadir un par de parámetros al archivo de configuración:

*  La cantidad máxima de memoria a utilizar, `maxmemory`
*  Algoritmo a utilizar en el caso de un overflow, `maxmemory-policy`

Editar `redis.conf`

```bash
$ sudo vim /etc/redis/redis.conf
...
#128_MB_max_memory
maxmemory 128mb
# When mem overflow remove according to LRU algorithm
maxmemory-policy allkeys-lru
```
Iniciar el servicio Redis

### Redis cli

`redis-cli` is the Redis command line interface, a simple program that allows to send commands to Redis, and read the replies sent by the server, directly from the terminal.

```bash
superset@asidvizint:/etc/nginx> redis-cli
127.0.0.1:6379> ping
PONG
127.0.0.1:6379>
```
# Superset, Celery y Redis

Todos los servicios están activos, vamos a configurar Superset para disponer de un sistema que sea escalable y distribuido.

Editamos el archivo principal de configuación de Superset, `config.py`

```python

# Comentamos estas lineas
# CELERY_CONFIG = None
# SQL_CELERY_DB_FILE_PATH = os.path.join(DATA_DIR, 'celerydb.sqlite')
# SQL_CELERY_RESULTS_DB_FILE_PATH = os.path.join(DATA_DIR, 'celery_results.sqlite')

# Celery & Redis cache

from werkzeug.contrib.cache import RedisCache

# Cache de mapas
MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY', 'pk.eyJ1IjoiY2NlcmNvcyIsImEiOiJjamNyeG4xZ2cyeDVzMnJueGh3cDk3bjc4In0.K7X-yR7rMJPzumJscjKRKQ')

CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 120,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 1,
    'CACHE_REDIS_URL': 'redis://localhost:6379/1'}

class CeleryConfig(object):
    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_IMPORTS = ('superset.sql_lab', )
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}

CELERY_CONFIG = CeleryConfig

RESULTS_BACKEND = RedisCache(
    host='localhost',
    port=6379,
    key_prefix='superset_results'
)
```
Se puede comprobar la doble funcion de Redis, broker y caché y el paso de mensajes desde Celery a Redis.

# Puesta en marcha de la arquitectura

El orden de inicio de los distintos sistemas que forman la arquitectura puede ser el siguiente:

*  Nginx, iniciado como servicio
*  Redis, iniciado como servicio
*  Gunicorn, iniciar desde consola (puede ser configurado como [servicio](http://docs.gunicorn.org/en/stable/deploy.html#monitoring)) 
*  Celery, configurado en Superset
*  Superset, se inicia desde Gunicorn

Por tanto, queda iniciar Gunicorn
```bash
superset@asidvizint:~> gunicorn -w 5 -k gevent --timeout 120 -b 0.0.0.0:8000 superset:app
[2018-08-22 12:41:23 +0200] [27180] [INFO] Starting gunicorn 19.9.0
[2018-08-22 12:41:23 +0200] [27180] [INFO] Listening at: http://0.0.0.0:8000 (27180)
[2018-08-22 12:41:23 +0200] [27180] [INFO] Using worker: gevent
[2018-08-22 12:41:23 +0200] [27183] [INFO] Booting worker with pid: 27183
[2018-08-22 12:41:23 +0200] [27184] [INFO] Booting worker with pid: 27184
[2018-08-22 12:41:23 +0200] [27185] [INFO] Booting worker with pid: 27185
[2018-08-22 12:41:23 +0200] [27188] [INFO] Booting worker with pid: 27188
[2018-08-22 12:41:23 +0200] [27189] [INFO] Booting worker with pid: 27189
```

# Comprobando el sistema de Cache

Realizamos varias consultas desde Superset y comprobamos

![asidvizintCache](/uploads/f058725e2d456fa500846868d2e488ae/asidvizintCache.png)