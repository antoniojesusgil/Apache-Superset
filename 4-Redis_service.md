# Redis como servicio

### Comprobar servicio

`as root` o bien usando `sudo`
```sh
host:~ # systemctl status redis@
Failed to get properties: Unit name redis@.service is neither a valid invocation ID nor unit name.
```

### Habilitar

```sh
host:~ # systemctl enable redis@
Created symlink /etc/systemd/system/graphical.target.wants/redis@.service → /usr/lib/systemd/system/redis@.service.
Created symlink /etc/systemd/system/multi-user.target.wants/redis@.service → /usr/lib/systemd/system/redis@.service.
Created symlink /etc/systemd/system/redis.target.wants/redis@.service → /usr/lib/systemd/system/redis@.service.
```

### Iniciar

```bash
host:~ # systemctl start redis.target
host:~ # systemctl status redis.target
● redis.target - Redis target allowing to start/stop all redis@.service instances at once
   Loaded: loaded (/usr/lib/systemd/system/redis.target; static; vendor preset: disabled)
   Active: active since Fri 2019-01-11 13:26:12 CET; 9s ago

Jan 11 13:26:12 host systemd[1]: Reached target Redis target allowing to start/stop all redis@.service instances at once.
```

# Monitorización Redis mediante AppManager

Comprobar servicio y la dirección de esucha

```bash
host:~ # ps -ef | grep redis
redis     1224     1  0  2018 ?        00:34:18 /usr/sbin/redis-server 127.0.0.1:6379
root     31606 31525  0 13:27 pts/0    00:00:00 grep redis
host:~ # netstat -naop | grep 6379
tcp        0      0 127.0.0.1:6379          0.0.0.0:*               LISTEN      1224/redis-server 1  off (0.00/0/0)
```
Comprobamos que está `off` la escucha a cualquier conexión. Para ello se modifica el archivo de configuración `redis.conf` y se cambia la opción `bind` en la sección `NETWORK`

```conf
bind 0.0.0.0
```
reiniciar el servicio y comprobar
```bash
host:~ # systemctl stop redis.target
host:~ # systemctl status redis.target
● redis.target - Redis target allowing to start/stop all redis@.service instances at once
   Loaded: loaded (/usr/lib/systemd/system/redis.target; static; vendor preset: disabled)
   Active: inactive (dead) since Fri 2019-01-11 13:36:48 CET; 6s ago

Jan 11 13:35:53 host systemd[1]: Reached target Redis target allowing to start/stop all redis@.service instances at once.
Jan 11 13:36:48 host systemd[1]: Stopped target Redis target allowing to start/stop all redis@.service instances at once.
host:~ # systemctl start redis.target
host:~ # ps -ef | grep redis
redis    31702     1  0 13:37 ?        00:00:00 /usr/sbin/redis-server 0.0.0.0:6379
root     31708 31525  0 13:37 pts/0    00:00:00 grep redis
```