# core/settings_prod.py
"""Configuración de producción para Render.

Hereda core/settings.py y sobreescribe lo necesario para producción.

Variables de entorno requeridas en Render:
    SECRET_KEY              -> clave aleatoria de al menos 50 caracteres
    DATABASE_URL            -> URL de PostgreSQL (la da Render PostgreSQL)
    DJANGO_SETTINGS_MODULE  -> core.settings_prod
    ALLOWED_HOSTS           -> dominio extra (opcional, separado por comas)
"""
import os

import dj_database_url

from .settings import *  # noqa: F401,F403

# ── Seguridad básica ──────────────────────────────────────────────────────
DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']  # falla a propósito si no existe

# ── Hosts permitidos ──────────────────────────────────────────────────────
# Render inyecta RENDER_EXTERNAL_HOSTNAME automáticamente.
_render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')
_extra_hosts = os.environ.get('ALLOWED_HOSTS', '').split(',')

ALLOWED_HOSTS = ['localhost', '127.0.0.1'] + (
    [_render_host] if _render_host else []
) + [h for h in _extra_hosts if h]

# ── Proxy de Render ───────────────────────────────────────────────────────
# Render termina el SSL antes de llegar a Django. Sin esta línea,
# SECURE_SSL_REDIRECT provoca un bucle de redirecciones.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ── Base de datos: PostgreSQL vía DATABASE_URL ────────────────────────────
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
}

# ── CSRF: dominios de confianza ───────────────────────────────────────────
CSRF_TRUSTED_ORIGINS = []
if _render_host:
    CSRF_TRUSTED_ORIGINS.append(f'https://{_render_host}')

# ── Cabeceras HTTP seguras ────────────────────────────────────────────────
SECURE_SSL_REDIRECT            = True
SECURE_HSTS_SECONDS            = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD            = True
SESSION_COOKIE_SECURE          = True
CSRF_COOKIE_SECURE             = True
X_FRAME_OPTIONS                = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF    = True
SECURE_REFERRER_POLICY         = 'same-origin'

# ── Archivos estáticos ────────────────────────────────────────────────────
# Sin manifiesto: WhiteNoise sirve los archivos sin validar hashes.
# Evita "Missing staticfiles manifest entry" (ValueError, 500) en Render.
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

# ── Logging: solo WARNING y superiores ────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '[%(levelname)s] %(name)s: %(message)s'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django.security': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}