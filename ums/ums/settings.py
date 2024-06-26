from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-06)qd6hk$1ww)523iwqon00olxgkeyarocomswba5xs-==1)l9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',    ## magic happens here
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth.socialaccount',

    'app',
    # Required by allauth.
    'django.contrib.sites',


    # Enable allauth.
    'allauth',
    'allauth.account',

    # Configure the django-otp package.
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_email',
    'django_otp.plugins.otp_totp',

    # Enable two-factor auth.
    'allauth_2fa',
    'django.contrib.humanize',
    'allauth.usersessions',
    'crispy_forms',

    'allauth.mfa',
    'django_countries',
    'axes',
    'django_user_agents',  ### identify the user devices
    'django_seed',
]

CRISPY_TEMPLATE_PACK = 'uni_form'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'allauth_2fa.middleware.AllauthTwoFactorMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware:
    'allauth.account.middleware.AccountMiddleware',

    # Optional -- needed when: USERSESSIONS_TRACK_ACTIVITY = True
    'allauth.usersessions.middleware.UserSessionsMiddleware',
    'axes.middleware.AxesMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',

]
USERSESSIONS_TRACK_ACTIVITY = True
ACCOUNT_ADAPTER = 'allauth_2fa.adapter.OTPAdapter'

ROOT_URLCONF = 'ums.urls'
import os
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
    'axes.backends.AxesStandaloneBackend',
]


WSGI_APPLICATION = 'ums.wsgi.application'

SITE_ID = 1
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Using email as username
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # 'optional' or 'none'
ACCOUNT_CHANGE_EMAIL = False

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
EMAIL_USE_TLS = True

ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
AUTH_USER_MODEL = 'app.Customuser'
ACCOUNT_FORMS = {
    'signup': 'app.forms.CustomSignupForm',
}

TIME_ZONE = 'Australia/Brisbane'
USE_TZ = True

# settings.py
# Set session to expire after 1 hour of inactivity
# Session timeout settings
SESSION_COOKIE_AGE = 3000  # Set session to expire after 30 seconds of inactivity
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Session expires on browser close

# Django Allauth settings for session management
ACCOUNT_SESSION_REMEMBER = None  # Whether to remember the user's session. None means use the session expiry settings
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True  # Log out users when they change their password
ACCOUNT_LOGOUT_ON_GET = True

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1  # Email confirmation links expire in 1 day
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True  # Use HMAC for email confirmation tokens
ACCOUNT_EMAIL_NOTIFICATIONS = True

from datetime import timedelta


AXES_FAILURE_LIMIT = 2  # Number of allowed failed login attempts.
AXES_COOLOFF_TIME = timedelta(minutes=30)  # Lockout period once the limit is exceeded.
AXES_RESET_ON_SUCCESS = True  # Resets the number of failed attempts after a successful login.
AXES_LOCKOUT_TEMPLATE = 'account/lockout.html'

