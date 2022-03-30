from .base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_)44b(ia1jzi42a1nz=ma@b(!94ase%x@@j_5^7puo!bws*a=%'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'NAME': 'oddam_w_dobre_rece',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'PASSWORD': 'coderslab',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'tomasz.bladyniec@gmail.com'
EMAIL_HOST_PASSWORD = 'frmkjqjmmbxuqjip'
EMAIL_PORT = 587
