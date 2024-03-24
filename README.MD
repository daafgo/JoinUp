# Test Join Up
Las librerias necesarias para la ejecucion de este codigo se encuentran en el fichero requirements.txt, para instalarlo utiliza el siguiente comando:

`pip install -r requirements.txt`

## Entornos
La aplicacion esta configurada para obtener las variables de entorno desde dos ficheros, .env en caso de produccion o .env.dev en caso de test y development.Se incluyen todas la variables de entorno necesarias en el fichero .env.dev

## Ejecución de test
ENV=dev python manage.py test

### config de Celery
Junto al proyecto contamos con un docker-compose para montar un servidor de redis
ejecutalo utilizando `compose-up -d`

a continuacion ejecuta el siguiente comando para tener un worker de celery escuchando

`celery -A JoinUpTest worker --loglevel=info`

