# Superset
Procedimiento para poner en marcha Superset

## Acciones de Sistema Operativo

### Crear usuario
Crear un usuario de sistema que pertenezca a sudoers (visudo)

### Librerias y dependencias de SSOO (sles 15)

#### python3-devel
```
 zypper in python3-devel
Loading repository data...
Reading installed packages...
Resolving package dependencies...

The following NEW package is going to be installed:
  python3-devel
```
#### gcc gcc-c++ 
```
zypper in gcc gcc-c++
Loading repository data...
Reading installed packages...
Resolving package dependencies...

The following 15 NEW packages are going to be installed:
  gcc gcc-c++ gcc7 gcc7-c++ libasan4 libatomic1 libcilkrts5 libgomp1 libitm1 liblsan0 libmpx2 libmpxwrappers2 libstdc++6-devel-gcc7 libtsan0
  libubsan0

15 new packages to install.
Overall download size: 36.4 MiB. Already cached: 0 B. After the operation, additional 135.5 MiB will be used.
Continue? [y/n/...? shows all options] (y):
```
#### libopenssl
```
zypper in libopenssl-devel
Loading repository data...
Reading installed packages...
Resolving package dependencies...

The following NEW package is going to be installed:
  libopenssl-devel
```
#### libffi-devel openldap2-devel sasl-devel
```
 zypper in libffi-devel openldap2-devel
Loading repository data...
Reading installed packages...
Resolving package dependencies...

The following 3 NEW packages are going to be installed:
  cyrus-sasl-devel libffi-devel openldap2-devel
```
#### libmysqld-devel
``` 
zypper in libmysqld-devel
```

### Librerias Python 3.x

#### Actualizar setuptools & pip
```
pip3 install --upgrade setuptools
```
```
pip install --upgrade pip
Collecting pip
  Downloading https://files.pythonhosted.org/packages/d8/f3/413bab4ff08e1fc4828dfc59996d721917df8e8583ea85385d51125dceff/pip-19.0.3-py2.py3-none-any.whl (1.4MB)
    100% |████████████████████████████████| 1.4MB 642kB/s
Installing collected packages: pip
  Found existing installation: pip 10.0.1
    Uninstalling pip-10.0.1:
      Successfully uninstalled pip-10.0.1
Successfully installed pip-19.0.3
```
#### python-ldap
```
 # pip3 install python-ldap
Collecting python-ldap
  Using cached https://files.pythonhosted.org/packages/7f/1c/28d721dff2fcd2fef9d55b40df63a00be26ec8a11e8c6fc612ae642f9cfd/python-ldap-3.1.0.tar.gz
Requirement already satisfied: pyasn1>=0.3.7 in /usr/lib/python3.6/site-packages (from python-ldap) (0.4.2)
Requirement already satisfied: pyasn1_modules>=0.1.5 in /usr/lib/python3.6/site-packages (from python-ldap) (0.2.4)
Installing collected packages: python-ldap
  Running setup.py install for python-ldap ... done
Successfully installed python-ldap-3.1.0
```
### Drivers para databases
#### Mysql
```
pip3 install mysqlclient
```
#### IBM DB2
```
pip3 install ibm_db
```
```
pip3 install ibm_db_sa
```
#### Gevent
```
pip3 install gevent
```
## Superset
Instalar la última versión liberada
```
pip3 install superset
```
Instalar una versión concreta
```
pip3 install superset==0.27.0
Collecting superset==0.27.0
```
### Error en instalación

`Command "python setup.py egg_info" failed with error code 1 in /tmp/pydruid/`

Este error viene dado por la utilización de un proxy sin acceso a los repositiorios python.

### Incompatibilidades
```
flask-appbuilder 1.10.0 has requirement click==6.7, but you'll have click 7.0 which is incompatible.
flask-appbuilder 1.10.0 has requirement colorama==0.3.9, but you'll have colorama 0.4.1 which is incompatible.
```
Se han de degradar las versiones
```
pip3 install click==6.7
pip3 install colorama==0.3.9
```

### Configuración básica

#### Superset db
Por defecto utiliza un sqlite. En caso de querer cambiar a postgresql o mysql, se debe crear una base de datos y un usuario con privilegios para ser gestionada.

```
MariaDB [(none)]> create database superset;
Query OK, 1 row affected (0.00 sec)

MariaDB [(none)]> GRANT ALL PRIVILEGES ON superset.* TO superset@'localhost' identified by 'xxxxx';
Query OK, 0 rows affected (0.00 sec)

MariaDB [(none)]> flush privileges;
Query OK, 0 rows affected (0.00 sec)
```
#### config.py
Editamos el archivo de configuración y cambiamos la bbdd. Superset utiliza SqlAlchemy
```
SQLALCHEMY_DATABASE_URI = 'mysql://superser:xxx@localhost/superset'
```
#### Iniciar Superset
El sistema se apoya en Flask y en el framework Flask-Appbuilder
```
fabmanager create-admin --app superset
Username [admin]: t2client
User first name [admin]: t2client
User last name [user]: admin-local
Email [admin@fab.org]: t2client-local@t2client.site
Password:
Repeat for confirmation:
```
El proceso genera un error 
```
Was unable to import superset Error: cannot import name '_maybe_box_datetimelike'
```

issue github --> https://github.com/apache/incubator-superset/issues/6770

Podemos obtar por una de estas soluciones (o ambas):

* Instalar pandas 0.23.4
* Modificar fichero `superset/dataframe.py`

```
vim /usr/lib/python3.6/site-packages/superset/dataframe.py
```
Una vez en el fichero hemos de encontrar la cadena `_maybe_box*` y sustituirla por `maybe_box*`

Si nos encontramos con el error markdown

`Was unable to import superset Error: markdown() takes 1 positional argument but 2 were given`

Este error hace referencia a que tenemos instalado un paquete markdown superior al que requiere superset y viene dado por el salto de versión de 0.26/27 a 0.28 o superior.

Solución:

```shell
pip3 install "markdown<3.0.0" superset
```
De esta forma indicamos que para Superset instale una versión de markdown inferior a 3.0

``` 
Installing collected packages: markdown
  Found existing installation: Markdown 3.0.1
    Uninstalling Markdown-3.0.1:
      Successfully uninstalled Markdown-3.0.1
Successfully installed markdown-2.6.11
```
Y repetimos el proceso de creación del usuario **administrador** 
Recordar el usuario y contraseña, los necesitaremos para acceder a la aplicación.

```
 fabmanager create-admin --app superset
Username [admin]: t2client
User first name [admin]: t2client
User last name [user]: local
Email [admin@fab.org]: t2client@t2client.com
Password:
```
```bash
Recognized Database Authentications.
Admin User t2client created.
```

Inicializar la base de datos

``` 
superset db upgrade
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 4e6a06bad7a8, Init
```
**Error**
```
sqlalchemy.exc.InvalidRequestError: Can`t determine...
````
Desinstalar SQLAlchemy e instalar la versión `1.2`

En este punto podemos cargar el dataset de ejemplos

```
superset load_examples
```
Por ultimo cargamos los roles por defecto y los permisos

```
superset init
2019-02-27 13:32:12,856:INFO:root:Creating database reference
2019-02-27 13:32:12,890:INFO:root:Syncing role definition
2019-02-27 13:32:12,942:INFO:root:Syncing Admin perms
2019-02-27 13:32:13,149:INFO:root:Syncing Alpha perms
2019-02-27 13:32:13,687:INFO:root:Syncing Gamma perms
2019-02-27 13:32:14,183:INFO:root:Syncing granter perms
2019-02-27 13:32:14,592:INFO:root:Syncing sql_lab perms
```

Llegados a este punto ya estaría disponible la aplicación, lo siguiente será dejar preparado el sistema para un entorno HA. (nginx, redis & gunicorn wsgi)

Para probar la aplicación podemos arrancar un servidor en modo `debug` mediante gunicorn o el propio superset

```
gunicorn -b 0.0.0.0:8088 superset:app
```
```
superset runserver -d
```