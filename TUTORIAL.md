mkdir ~/.venvs

python3 -m venv ~/.venvs/django

source ~/.venvs/django/bin/activate

pip install django gunicorn psycopg2-binary dj-database-url

pip freeze > requirements.txt

mkdir event-board-api

cd event-board-api

django-admin startproject config


Update config/settings.py.

```Python
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events', # Add events app to installed apps.
]
```

```Python
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    featured = models.BooleanField()
    hash_tag = models.CharField(max_length=200)

    def __str__(self):
        return self.title
```

Create migration for events
```
python manage.py makemigrations events
```

Migrate database
```
python manage.py migrate
```

Create superuser
```
python manage.py createsuperuser
```

config/settings.py

```
import os
```



STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"))


Setup debase configuration

```
if DEVELOPMENT_MODE is True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }
```


```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',
    'api',
]
```
