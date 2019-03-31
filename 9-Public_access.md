[Acceso publico](https://superset.incubator.apache.org/security.html?highlight=public#public)

# Acceso anónimo
It’s possible to allow logged out users to access some Superset features.

By setting `PUBLIC_ROLE_LIKE_GAMMA = True` in your superset_config.py, you grant public role the same set of permissions as for the GAMMA role. This is useful if one wants to enable anonymous users to view dashboards. Explicit grant on specific datasets is still required, meaning that you need to edit the Public role and add the Public data sources to the role manually.

# Gestión del rol Gamma para acceso a datasources
Here’s how to provide users access to only specific datasets. First make sure the users with limited access have [only] the Gamma role assigned to them. Second, create a new role (`Menu -> Security -> List Roles`) and click the `+` sign.

Veamos un ejemplo práctico de como crear un rol con acceso anónimo y acceso a datasources / dashboards.

Partimos de de tener activo `PUBLIC_ROLE_LIKE_GAMMA = True` en el archivo `config.py` y de haber comprobado el acceso anónimo a un dashboard en modo `standalone` (necesario aññadir el datasource al rol public)

Clonamos el rol `Public` o `Gamma` y comenzamos a quitar permisos sobre el nuevo rol `miRol`.

##### Nota: Existen dos tipos de permisos, sobre las vistas y sobre los base.

## Permisos más importantes
De todos los permisos resultantes en el nuevo rol los más importantes son:

`can user slices on Superset` -> Acceso a los charts creados por ese usuario

`can dashboard on Superset` -> Acceso a los dashboards

`can explore json on Superset` -> Sin este permiso no se mostraria ningun dato 

`can save dash on Superset` -> Se muestra el dashboard en modo raw sin css ni estilos

`can csrf token on Superset` -> Gestión del token

Y por supuesto, el rol debe tener acceso al datasource sobre el que se construye el dashboard.
