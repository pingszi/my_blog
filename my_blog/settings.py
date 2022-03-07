"""
Django settings for my_blog project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dbo1#dz$g%w(wo*7uw$h3$-&mj0qt1txns!y!rjd$-r)7_xy+l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'era_blog.apps.EraBlogConfig',
    'import_export',
    'mdeditor',
    'pure_pagination',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
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

ROOT_URLCONF = 'my_blog.urls'

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
                'era_blog.views.global_setting',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myblog',
        'HOST': 'www.pingswms.com',
        'PORT': '31001',
        'USER': 'root',
        'PASSWORD': 'Zhou1182969',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# 语言时区
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# 日志记录
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(name)s %(funcName)s %(lineno)d %(message)s',
            'datefmt' :"%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR + '/logs/', 'erablog.log'),
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else "INFO",
        },
        'django.db.backends': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else "INFO",
        },
        'erablog': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else "INFO",
        },
    }
}

# 静态文件配置
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 网站的基本信息配置
SITE_NAME = 'Pings博客'         # 站点名称
SITE_DESCRIPTION = 'Pings博客'  # 站点描述
SITE_KEYWORDS = 'python,django,java,spring,微服务,博客'    # 站点关键词
SITE_TITLE = 'Pings博客'        # 博客标题
SITE_TYPE_CHINESE = 'Pings的博客, 仅用于开发技术交流'  # 打字效果 中文内容
SITE_TYPE_ENGLISH = 'python django java spring springcloud dubbo docker k8s'  # 打字效果 英文内容
SITE_MAIL = '275598139@qq.com'  # 我的邮箱
SITE_ICP = '粤ICP备18148895号'   # 网站备案号 
SITE_ICP_URL = 'http://beian.miit.gov.cn'  # 备案号超链接地址  

# Simple Ui 相关设置
SIMPLEUI_LOGIN_PARTICLES = False
SIMPLEUI_ANALYSIS = False
SIMPLEUI_STATIC_OFFLINE = True
SIMPLEUI_LOADING = False
SIMPLEUI_LOGO = 'https://image.3001.net/images/20191031/15724874583730.png'
# **菜单图标
SIMPLEUI_ICON = {
    '文章分类': 'fa fa-folder',
    '文章标签': 'fa fa-tag'
}

# **七牛云配置
# QINIU_ACCESS_KEY = '' # AccessKey
# QINIU_SECRET_KEY = '' # SecretKey
QINIU_BUCKET_NAME = 'pings-static-file'  # 存储空间名字
QINIU_BUCKET_DOMAIN = 'static.pings.fun' # 外链默认域名
QINIU_SECURE_URL = False # 使用http

PREFIX_URL = 'http://'
MEDIA_URL = PREFIX_URL + QINIU_BUCKET_DOMAIN + "/myblog/media/"
MEDIA_ROOT = 'myblog/media/'
DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuMediaStorage'  # 文件系统更改

#**django mysql客户端默认为mysqlclient，比较难安装。使用pymysql替换mysqlclient
import pymysql
pymysql.install_as_MySQLdb()
