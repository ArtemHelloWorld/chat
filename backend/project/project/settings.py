import datetime
import os
import pathlib

import dotenv

dotenv.load_dotenv()
TRUE_VALUES = {"", "true", "yes", "y", "1"}

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'some_fake_key')

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in TRUE_VALUES

EVENTSTREAM_ALLOW_ORIGIN = '*'

ALLOWED_HOSTS = [
    host.strip() for host in os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'django_eventstream',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'chat.apps.ChatConfig',
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'drf_yasg',
]
CORS_ALLOW_ALL_ORIGINS = True

ASGI_APPLICATION = 'project.asgi.application'

CHANNEL_LAYERS = {
    'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}
}
MIDDLEWARE = [
    'django_grip.GripMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'project.middleware.custom.RateLimitMiddleware',
]

RATE_LIMIT_MIDDLEWARE = os.getenv(
    'RATE_LIMIT_MIDDLEWARE', 'False'
).lower() in TRUE_VALUES
REQUESTS_PER_SECOND = int(os.getenv('REQUESTS_PER_SECOND', 10))

ROOT_URLCONF = 'project.urls'


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

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.'
            'password_validation.UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.'
            'password_validation.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.'
            'password_validation.NumericPasswordValidator'
        ),
    },
]


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': '',
    'AUDIENCE': None,
    'ISSUER': None,
    'JSON_ENCODER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': (
        'rest_framework_simplejwt.authentication.'
        'default_user_authentication_rule'
    ),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=90),
    'TOKEN_OBTAIN_SERIALIZER': (
        'rest_framework_simplejwt.serializers.TokenObtainPairSerializer'
    ),
    'TOKEN_REFRESH_SERIALIZER': (
        'rest_framework_simplejwt.serializers.TokenRefreshSerializer'
    ),
    'TOKEN_VERIFY_SERIALIZER': (
        'rest_framework_simplejwt.serializers.TokenVerifySerializer'
    ),
    'TOKEN_BLACKLIST_SERIALIZER': (
        'rest_framework_simplejwt.serializers.TokenBlacklistSerializer'
    ),
    'SLIDING_TOKEN_OBTAIN_SERIALIZER': (
        'rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer'
    ),
    'SLIDING_TOKEN_REFRESH_SERIALIZER': (
        'rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer'
    ),
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.' 'password_validation.MinimumLengthValidator'
        ),
        'OPTIONS': {
            'min_length': 8,
        },
    },
    {
        'NAME': (
            'django.contrib.auth.'
            'password_validation.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.'
            'password_validation.NumericPasswordValidator'
        ),
    },
]

SWAGGER_SETTINGS = {
    'LOGIN_URL': '/api-auth/login/',
    'LOGOUT_URL': '/api-auth/logout/',
}
