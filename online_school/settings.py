from pathlib import Path
from decouple import config
import os
from datetime import timedelta
import cloudinary

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*joid9m4y#gsg^#3qdcn%5ugh4!d!irp%&y2tm4_x2o#=t6)h3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    ".vercel.app",
    
    ".now.sh",
    "127.0.0.1",
    "localhost",
    "online-school-backend-1.onrender.com",

]
AUTH_USER_MODEL = 'users.User'

# Application definition

INSTALLED_APPS = [
     'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
     "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',
    'rest_framework',
    'api',
    'adminApp',
    'course',
    'order',
    'users',
    'djoser',
    "corsheaders",
    'drf_yasg',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
     "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE:"whitenoise.storage.CompressedStaticFilesStorage"

ROOT_URLCONF = 'online_school.urls'

CORS_ALLOWED_ORIGINS = [
  "http://127.0.0.1:8000",
  "http://localhost:5173",
  "https://online-school-backend-1.onrender.com",
   "https://online-school-frontend-wbqk.vercel.app",

]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'online_school.wsgi.app'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('dbname'),
        'USER': config('user'),
        'PASSWORD': config('password'),
        'HOST': config('host'),
        'PORT': config('port')
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        
       'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

  
}



SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT',),
   "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),


}


DJOSER = {
     'EMAIL_FRONTEND_PROTOCOL':config('FRONTEND_PROTOCOL'),
    'EMAIL_FRONTEND_DOMAIN':config('FRONTEND_DOMAIN'),
    'EMAIL_FRONTEND_SITE_NAME':'Online School',
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SERIALIZERS': {
   
        'user_create':'users.serializers.UserCreateSerializer',
        'current_user':'users.serializers.UserSerializer'
 },
    'EMAIL_FRONTEND_PROTOCOL':config('FRONTEND_PROTOCOL'),
    'EMAIL_FRONTEND_DOMAIN':config('FRONTEND_DOMAIN'),
    'EMAIL_FRONTEND_SITE_NAME':'Online School',
   
}

# SWAGGER_SETTINGS = {
#     'DEFAULT_FILTER_INSPECTORS': [
#         'drf_yasg.inspectors.DjangoFilterInspector',
#         'drf_yasg.inspectors.CoreAPICompatInspector',
#     ],
# }



# AUTHENTICATION_BACKENDS = ["djoser.auth_backends.LoginFieldBackend",]

EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_HOST_USER = 'p29m35@gmail.com'
EMAIL_HOST_PASSWORD = 'lgwt oexg qemd zjbs'

BACKEND_URL = config("BACKEND_URL")
FRONTEND_URL = config("FRONTEND_URL")

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
# STATICFILES_DIRS = [
#         BASE_DIR / "static",
#     ]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Configuration       
cloudinary.config( 
    cloud_name = config('Cloud_name'), 
    api_key = config("API_key"), 
    api_secret = config("API_secret"), 
    # CLOUDINARY_URL= config("CLOUDINARY_UR"),
    secure=True

)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
    #   'Basic': {
    #         'type': 'basic'
    #   },
      'JWT': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description':'Enter Your token in the format `JWT<token>`'
      }
   }
}