"""
Django settings para App_Gestion_Escolar.

Este archivo es el "reglamento escolar" de nuestro proyecto.
Aquí Django aprende todo: qué apps existen, dónde están los templates,
dónde están los archivos estáticos (CSS), etc.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-clave-solo-para-desarrollo-cambiala-en-produccion'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'alumnos',
    'profesores',
    'cursos',
    'predicciones',
    'notas',
    'apoderados',
    'planificaciones',
    'pie',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'App_Gestion_Escolar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'App_Gestion_Escolar.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Seguridad — Variables de Autenticación (UNA SOLA VEZ)
# ---------------------------------------------------------------------------
LOGIN_REDIRECT_URL  = '/'   # ← Al loguearse va al panel de inicio
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL           = 'login'

# ── Correo electrónico ──
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = 'tu_correo@gmail.com'      # ← cambia esto
EMAIL_HOST_PASSWORD = 'tu_contraseña_de_app'     # ← cambia esto (contraseña de aplicación Gmail)
DEFAULT_FROM_EMAIL  = 'Liceo Municipal <tu_correo@gmail.com>'