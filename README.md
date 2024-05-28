# Creacion del proyecto

## Primeros pasos
  - se crea el entorno virtual (save_library)
  - instala django
  - se crea el proyecto (django_save_library)

## Extensiones instaladas

```` bash
# Python-DotEnv (no se uso (creo Xd))
  pip install python-dotenv
#
````
## Crear la aplicacion

```bash
python manage.py startapp ecommerce
```

## Configurar SQL

````
CLOUDINARY_CLOUD_NAME = 'dza7bp5ku',
CLOUDINARY_API_KEY = '651588235946771',
CLOUDINARY_API_SECRET = 'zddmEi3l-KnKsgn2Na_93GqWf80',
DB_NAME = 'django_save_library'
DB_USER = 'postgres'
DB_PASSWORD = 'route'
DB_HOST = 'localhost'
DB_PORT = '5432'
````

```` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}
````

## Integral la DataBase

### Primera migracion

### Migrar los modelos de la App

## Unir el Cloudinary
