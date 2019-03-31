# Gunicorn como servicio

## gunicorn.conf

[Doc oficial](http://docs.gunicorn.org/en/stable/configure.html)

[Settings](http://docs.gunicorn.org/en/stable/settings.html#config-file)

### Server socket
Gunicorn puede ser configurado bien mediante conexión de red TCP o socket unix. 
[más información](https://serverfault.com/questions/124517/whats-the-difference-between-unix-socket-and-tcp-ip-socket) también se puede implementar este [IPC Benchmark](https://github.com/rigtorp/ipc-bench) para comprobar la latencia.

### Logging
Crear estructura de logs en /var/log/gunicorn y dar permisos necesarios.
 
## Chequear archivo de configuración: 
`gunicorn --check-config`

## Archivo systemD
[Información sobre systemd](https://www.freedesktop.org/wiki/Software/systemd/)

### Creamos el servicio

`superset@host:~> cd /etc/systemd/system/`
`superset@host:/etc/systemd/system> sudo touch gunicorn.service`

```script
Description=Gunicorn daemon para servir Superset
After=network.target

[Service]
PermissionsStartOnly=true
PIDFile=/run/gunicorn/pid
User=superset
Group=users
RuntimeDirectory=gunicorn
WorkingDirectory=/usr/lib/python3.6/site-packages/superset
ExecStart=/usr/bin/gunicorn -c /etc/gunicorn/gunicorn.conf --pid /run/gunicorn/pid --bind unix:/run/gunicorn/socket superset:app
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s HUP $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```
### Reload de los daemons
`systemctl daemon-reload`

### Iniciar gunicorn service
`systemctl start gunicorn.service`

```
superset@host:/etc/systemd/system> systemctl start gunicorn.service
==== AUTHENTICATING FOR org.freedesktop.systemd1.manage-units ====
Se requiere autenticación para iniciar 'gunicorn.service'.
Authenticating as: root
Password:
==== AUTHENTICATION COMPLETE ====
```

## Comprobar los servicios

systemctl status gunicorn.service

## systemD 

Veamos cómo administrar los servicios en una distribución de Linux con SystemD:

* A modo de ejemplo, utilizaremos como nombre de servicio: sshd 

- Lista todos los servicios: 

systemctl list-units -t service --all

- Lista solo los servicios activos: 

systemctl list-units -t service

- Verifica el estado de un servicio: 

systemctl status sshd.service

- Indica si un servicio está o no activo: 

systemctl is-active sshd.service

- Muestra las dependencias de un archivo: 

systemctl list-dependencies sshd.service

- Inicia un servicio: 

systemctl start sshd.service

- Detiene un servicio: 

systemctl stop sshd.service

- Reinicia un servicio: 

systemctl restart sshd.service

- Recarga cambios en la configuración de un servicio (aplica cambios en la configuración del servicio sin reiniciarlo): 

systemctl reload sshd.service

- Enmascara un servicio (Evita que otro servicio pueda iniciarlo): 

systemctl mask sshd.service

- Desenmascara un servicio (Deshace el enmascarado del servicio): 

systemctl unmask sshd.service

- Configura el inicio automático de un servicio: 

systemctl enable sshd.service

- Quita el inicio automático de un servicio: 

systemctl disable sshd.service