from pathlib import Path
import os

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as messages

gettext = lambda s: s

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
    'shop.apps.ShopConfig',
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
    'ads',
    'sekizai',
    'payment.apps.PaymentConfig',
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

TIME_ZONE = 'Africa/Lagos'

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
#EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend" # In Production environment
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  #465
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bioscomsoft@gmail.com'
EMAIL_HOST_PASSWORD = 'qqboykvpqsffmnxs'
#EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#   Verify user email address  https://pypi.org/project/Django-Verify-Email/#step3     
EXPIRE_AFTER = "5d" # Will expire after five days from link generation
MAX_RETRIES = 10 
HTML_MESSAGE_TEMPLATE = "account/partial_email_verification_message.html"
VERIFICATION_SUCCESS_TEMPLATE = "account/partial_verification_successful.html"
VERIFICATION_FAILED_TEMPLATE = "account/partial_email_verification_failed.html"
REQUEST_NEW_EMAIL_TEMPLATE = 'account/partial_request_new_email.html'
LINK_EXPIRED_TEMPLATE = 'account/partial_link_expired.html'
NEW_EMAIL_SENT_TEMPLATE = 'account/partial_new_email_sent.html'
SUBJECT = 'Email Verification Mail' # can be changed later
#   end of user email address verification


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


MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


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
        'height': 250,
        'width': '100%',
        'removePlugins':'resize',
        'resize_enabled':'false',
        'removePlugins':'elementspath',
        'youtube_responsive':'true',
        'filebrowserWindowHeight': 725,
        'filebrowserWindowWidth': 940,
        'allowedContent': True,
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
            'youtube',
            'html5video',
            #'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'mediaembed',
            #'elementspath'
        ]),
    }
}


ADS_GOOGLE_ADSENSE_CLIENT = None  # 'ca-pub-xxxxxxxxxxxxxxxx'

ADS_ZONES = {
    'header': {
        'name': gettext('Header'),
        'ad_size': {
            'xs': '720x150',
            'sm': '800x90',
            'md': '800x90',
            'lg': '800x90',
            'xl': '800x90'
        },
        'google_adsense_slot': None,  # 'xxxxxxxxx',
        'google_adsense_format': None,  # 'auto'
    },
    'content': {
        'name': gettext('Content'),
        'ad_size': {
            'xs': '720x150',
            'sm': '800x90',
            'md': '800x90',
            'lg': '800x90',
            'xl': '800x90'
        },
        'google_adsense_slot': None,  # 'xxxxxxxxx',
        'google_adsense_format': None,  # 'auto'
    },
    'sidebar': {
        'name': gettext('Sidebar'),
        'ad_size': {
            'xs': '720x150',
            'sm': '800x90',
            'md': '800x90',
            'lg': '800x90',
            'xl': '800x90'
        }
    }
}

ADS_DEFAULT_AD_SIZE = '720x150'

ADS_DEVICES = (
    ('xs', _('Extra small devices')),
    ('sm', _('Small devices')),
    ('md', _('Medium devices (Tablets)')),
    ('lg', _('Large devices (Desktops)')),
    ('xl', _('Extra large devices (Large Desktops)')),
)

ADS_VIEWPORTS = {
    'xs': 'd-block img-fluid d-sm-none',
    'sm': 'd-none img-fluid d-sm-block d-md-none',
    'md': 'd-none img-fluid d-md-block d-lg-none',
    'lg': 'd-none img-fluid d-lg-block d-xl-none',
    'xl': 'd-none img-fluid d-xl-block',
}


# Braintree settings
BRAINTREE_MERCHANT_ID = '7vybxjn8qbyqpyfk' # Merchant ID
BRAINTREE_PUBLIC_KEY = 'wt3c8z3wv33hf8c6' # Public Key
BRAINTREE_PRIVATE_KEY = '7c99947c2887b47a062c8f86fa9ba7c2' # Private key

import braintree

BRAINTREE_CONF = braintree.Configuration(
    braintree.Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)