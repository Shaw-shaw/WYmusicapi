"""
Django settings for HHHmusicapi project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import sys
# 不添加到环境变量  会抛异常
# OSError: [WinError 123] 文件名、目录名或卷标语法不正确。: '<frozen importlib._bootstrap>'
sys.path.append(os.path.join(BASE_DIR, 'apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd^yfqf2fsfgjkt4w$kb3)-b@)*%ia*e27#sfuj(j9s*2$!@ndw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
# celery peizhi
# from djagocele import celeryconfig
# BROKER_BACKEND='redis'
# BOOKER_URL='redis://127.0.0.1:6379/1'
# CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/2'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 自定义APP
    'user',
    'song',
    'video',
    # 第三方
    'rest_framework',
    'django_filters',
    'corsheaders',

    # xamin主体模块
    'xadmin',
    # 渲染表格模块
    'crispy_forms',
    # 为模型通过版本控制，可以回滚数据
    'reversion',
]

MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 允许跨域源
# CORS_ORIGIN_ALLOW_ALL = False
# 配置指定跨域域名
CORS_ORIGIN_WHITELIST = [
# 	'http://47.103.37.166:20',
#     'http://127.0.0.1:8000'
]

ROOT_URLCONF = 'HHHmusicapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'HHHmusicapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
#
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "USER": "root",
        "PASSWORD": "123",
        "NAME": "hhhmusic",
    }
}
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "HOST": "127.0.0.1",
#         "PORT": 3306,
#         "USER": "root",
#         "PASSWORD": "123",
#         "NAME": "hhhmusic2",
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",
        }
    }
}

# 日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            # 实际开发建议使用WARNING
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建，注：这里的文件路径要注意BASE_DIR
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/music.log"),
            # 日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件的数量,设置最大日志数量为10
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
    },
    # 日志对象
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True, # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}

# 这里是固定写法：模块.继承AbstractUser的自定义User表
AUTH_USER_MODEL = 'user.User' # 将auth_user 换成我们的User表  'user.User'='app名.自己表名'

# 两个静态接口 MEDIA_URL可以保证用户上传到制定路径下
MEDIA_URL = "/media/"
# 项目中存储上传文件的根目录  MEDIA_ROOT
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# 配置多登录方式
# AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
AUTHENTICATION_BACKENDS = ['user.utils.utils.JWTModelBackend']

import datetime

# from rest_framework_jwt.utils import jwt_response_payload_handler

JWT_AUTH = {
    # 过期时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=11111111111),
    # 自定义认证结果：见下方序列化user和自定义response
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'user.utils.utils.jwt_response_payload_handler',
    # 一种给token加头的反扒策略 在authenticate中token获取方式就需要与之对应
    'JWT_AUTH_HEADER_PREFIX': '',
}

REST_FRAMEWORK = {
    # 认证模块
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'user.authentications.JSONWebTokenAuthentication',
    ),
    # 频率模块
    'DEFAULT_THROTTLE_RATES': {
        'sms': '1/m'
    },
}

# 云通讯配置
SMS_ACCOUNTSID = '8a216da86c282c6a016c5077c7051900'
SMS_ACCOUNTTOKEN = 'c2e4963468e14d6b920f34ecb2c18824'
SMS_APPID = '8a216da86c282c6a016c5077c75a1907'
SMS_SERVERIP = 'sandboxapp.cloopen.com'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
