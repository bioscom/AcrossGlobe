from pathlib import Path
import os

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ejcw-d5t67dgrz$_evfgd#kz7y_ku70urb5bnncn2^3*&o0l&@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#THUMBNAIL_DEBUG = True

ALLOWED_HOSTS = ['acrossglobe.com','localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'account.apps.AccountConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'django_extensions',
    'myblog',
    'django.contrib.humanize',
    'easy_thumbnails',
    'hitcount',
    'user_visit',
    'bootstrap_modal_forms',
    'widget_tweaks',
    'ckeditor',
    'ckeditor_uploader',
    'rosetta',
    'embed_video',
    'crispy_forms',
    'crispy_bootstrap4',
    'actions.apps.ActionsConfig',
    'verify_email.apps.VerifyEmailConfig',
    'phone_field',
    'django_social_share',
    #'herokuapp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'user_visit.middleware.UserVisitMiddleware',
    
]

ROOT_URLCONF = 'Blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["MyBlog/templates", "account/templates"],
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

WSGI_APPLICATION = 'Blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'acrossglobe', 
        'USER': 'postgres',
        'PASSWORD': 'Euaggelisis123',
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql',
#         'NAME': 'MyBlog',
#         # 'USER': '',
#         # 'PASSWORD': 'password',
#         # 'HOST': '192.168.2.17',
#         # 'PORT': '',
#         'OPTIONS': {
#             #'driver': 'ODBC Driver 13 for SQL Server',
#         },
#     },
# }  


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'myblog/media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = 'bootstrap4'



# Gmail SMTP Server
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend" # In Production environment

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'bioscomsoft@gmail.com'
EMAIL_HOST_PASSWORD = 'Euaggelisis@123'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EXPIRE_AFTER = "5d" # Will expire after ten days from link generation
#REQUEST_NEW_EMAIL_TEMPLATE = 'mytemplates/mycustomtemplate.html'  #To be investigated 
VERIFICATION_SUCCESS_TEMPLATE = None


LOGIN_REDIRECT_URL = 'https://acrossglobe.com:8000/'
LOGIN_URL = 'login'
LOGOUT_URL = 'https://acrossglobe.com:8000/'


# Social Authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
   #'account.authentication.EmailAuthBackend',
    'social_core.backends.facebook.FacebookOAuth2', 
    'social_core.backends.google.GoogleOAuth2', 
    'social_core.backends.twitter.TwitterOAuth',
    #'lazysignup.backends.LazySignupBackend',
]

# Facebook 
SOCIAL_AUTH_FACEBOOK_KEY = '1315611002498349' # Facebook App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'a553d902a532f01070cd72ee43af22e5' # Facebook App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

# Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '52838641831-91d3eiv8hggpsl6uptejbmn8v69bq8r8.apps.googleusercontent.com' # Google Consumer Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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' # Google Consumer Secret

# Twitter
SOCIAL_AUTH_TWITTER_KEY = '2304571970-D44Fw8W4azZirElg4s3s2vvBPwS1crlNUnUZ8lv' # Twitter API Key
SOCIAL_AUTH_TWITTER_SECRET = '4UzvOE9J3IIbSocjFPWnWb7EmsOptvEyboV9j2SWCLlCw' # Twitter API Secret


ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
}

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"
#CKEDITOR_FILENAME_GENERATOR = 'utils.get_filename'

# CKEDITOR_CONFIGS = {
#     'awesome_ckeditor': {
#         'toolbar': 'Basic',
#     },
# }

# CKEDITOR_CONFIGS={
#   'default': {
#     'skin': 'office2013',
#     'toolbar': 'Full',
#     'height': 500,
#     'width': '100%',
#     'extraPlugins':','.join(
#         [
#             'codesnippet', 'widget', 'youtube', 'html5video',
#         ]
#     ),
#   }
# }

CKEDITOR_CONFIGS = {
    'default': {
        #'skin': 'moono',
        'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'basicstyles', 'items': ['Source', 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert', 'items': ['Image', 'Flash', 'Html5video', 'Youtube', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            #{'name': 'about', 'items': ['About']},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
         'height': 300,
         'width': '100%',
         'youtube_responsive':'true',
         'filebrowserWindowHeight': 725,
         'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'youtube',
            'html5video',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

