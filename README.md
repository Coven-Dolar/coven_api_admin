### Entrar al usuario postgres

```
sudo -u postgres psql
```

### Crear un usuario para tu aplicación

```
CREATE USER coven_user WITH PASSWORD 'TuPasswordSegura123!';
```

### Crear la base de datos

```
CREATE DATABASE coven_db OWNER coven_user;
```

### Dar privilegios

```
GRANT ALL PRIVILEGES ON DATABASE coven_db TO coven_user;
```
