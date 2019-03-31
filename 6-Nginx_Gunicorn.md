# Nginx & Gunicorn

Se conectan mediante la directiva nginx `proxy_pass`

En este caso gunicorn está escuchando en un socket y todas las solicitudes enviadas por nginx son locales, por lo que el host que gunicorn 'entiende es 'localhost'.

Gunicorn debe crear la URL completa para cualquier envio o redirección. Debido a que solo conoce 'localhost', construirá la URL usando ese host.

Nginx se usa como puerta de enlace, por lo que es responsable de cambiar todas las URL de redirección enviadas para que coincidan con el nombre de dominio en el que nginx está sirviendo el sitio.

```nginx
upstream host {
    # Path to Unicorn SOCK file, as defined previously
    server unix:/run/gunicorn/socket fail_timeout=0;
}
server {
        listen       80;
        server_name  localhost;
        proxy_hide_header X-Frame-Options;
        
        location / {
                proxy_set_header Host $http_host;
                proxy_pass http://host;
        }
}
```