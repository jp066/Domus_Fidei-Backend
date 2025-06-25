from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-wtr7!g)y-4s72-gx6&h!6te*!o4$bx4owmv-f-)^u3#o^k^_ve'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST Framework
    'rest_framework.authtoken',  # Para autenticação via token, usando JWT
    'rest_framework_simplejwt',  # SimpleJWT
    'drf_yasg',  # Para documentação da API com Swagger
    'events',
    'finances',
    'pascom',
    'prayer_requests',
    'sacraments',
    'users',
    'cloudinary',         # adicionando Cloudinary 
    'cloudinary_storage', # adicionando Cloudinary Storage
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'drroo8xpo',  # Substitua pelo seu nome de nuvem do Cloudinary
    'API_KEY': '265219895429358',          # Substitua pela sua chave de API do Cloudinary
    'API_SECRET': '3PhW63CTrITd0EOnFAH7zyikunw',    # Substitua pelo seu segredo de API do Cloudinary
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Se você também quiser servir arquivos estáticos do Cloudinary (opcional)
# STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticCloudinaryStorage'
# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'  # Para collectstatic em produção
# 
# Diretórios adicionais onde o Django procura arquivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / 'static',
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

ROOT_URLCONF = 'Domus_Dei.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'Domus_Dei.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'domus_fidei',
        'USER': 'sa',
        'PASSWORD': 'domusdei123',
        'HOST': 'JOAOPEDRO\\SQLEXPRESS',  # Use the instance name if SQL Server is not the default instance
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'autocommit': True,  # essa configuração é necessária para evitar problemas de transação,
            'MARS_Connection': True,
        },
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True


STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROLEPERMISSIONS_MODULE = 'users.roles' # Define o módulo onde estão os papéis e permissões dos usuários
AUTH_USER_MODEL = 'users.Pessoa' # Define o modelo de usuário personalizado

# --- Configuração para arquivos de mídia (Imagens) ---
# Onde as imagens serão salvas no sistema de arquivos
MEDIA_ROOT = BASE_DIR / 'media'
# A URL para acessar esses arquivos de mídia
MEDIA_URL = '/media/'

# --- Configurações do Django REST Framework ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

ROTATE_REFRESH_TOKENS = True

# --- Configurações do Simple JWT ---
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=60), # Duração do token de acesso
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=10), # Duração do token de atualização
}