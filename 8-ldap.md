# Métodos Auth
Superset se apoya en `flask_appbuilder` para gestionar la autenticación, de entre todos los métodos que dispone se encuentra la conexión LDAP.

Para ello, se han de añadir al archivo `config.py` de Superset los métodos a utilizar:

```pyton
from flask_appbuilder.security.manager import AUTH_DB, AUTH_LDAP, AUTH_REMOTE_USER
```
**Importante:
Tan solo puede estar un método activo, por tanto se debe parar e iniciar la aplicación para disponer de cualquier otro que se quiera activar.

## LDAP

#### t2client

```python
# -----------------------------------------------------
# CONFIG t2client LDAP
# -----------------------------------------------------
AUTH_TYPE = AUTH_LDAP
AUTH_LDAP_SERVER = "ldap://130.10.90.40"
AUTH_LDAP_USE_TLS = False
AUTH_LDAP_SEARCH = "OU=People,OU=MUTUA,DC=t2client,DC=site"
#AUTH_LDAP_SEARCH = "dc=t2client,dc=org"
AUTH_LDAP_APPEND_DOMAIN = 't2client.org'
AUTH_LDAP_UID_FIELD = 'userPrincipalName'
AUTH_LDAP_FIRSTNAME_FIELD = 'givenName'
AUTH_LDAP_LASTNAME_FIELD = 'sn'
AUTH_LDAP_ALLOW_SELF_SIGNED = True
```