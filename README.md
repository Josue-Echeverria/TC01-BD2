# TC1 Docker Rest API

# Gestor de Tareas con Flask y PostgreSQL

Este proyecto es una aplicación web para la gestión de tareas. Utiliza Flask como framework de backend y PostgreSQL para la gestión de la base de datos.

## Características

- Autenticación de usuarios.
- Creación, actualización y eliminación de tareas.
- Visualización de tareas por usuario y por ID de tarea.

[Link del Api](http://localhost:5002)

# Commandos 

## Construye la imagen de docker

``` bash
docker build -t flask-restapi .
```

## Corre el contenedor de docker
``` bash
docker-compose -f docker-compose.dev.yml up --build
```

