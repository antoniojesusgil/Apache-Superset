# Gunicorn
Gunicorn se instala con superset. 

### Configuración
Crear directorio `/etc/gunicorn/gunicorn.conf`
Crear directorios de log `/var/log/gunicorn/access.log` y `/var/log/gunicorn/error.log`

Hacer propietario al usuario `superset` de `access.log` y `error.log`

### gunicorn.conf
```
import multiprocessing

# Server socket

#bind = '0.0.0.0:8000'
bind = 'unix:/run/gunicorn/socket'
backlog = 2048

# Worker processes

#workers = 5
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
worker_connections = 2048
timeout = 90
keepalive = 2

#   spew - Install a trace function that spews every line of Python

spew = False

# Server mechanics

daemon = False
pidfile = '/run/gunicorn/pid'
umask = 0
user = None
group = None
tmp_upload_dir = None

#   Logging

errorlog = '/var/log/gunicorn/error.log'
loglevel = 'debug'
accesslog = '/var/log/gunicorn/access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Processing Naming

proc_name = None

# Server hooks

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

    ## get traceback info
    import threading, sys, traceback
    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))

def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
```
