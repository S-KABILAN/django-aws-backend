from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------------
# SECURITY
# ----------------------------------------------------------------------
SECRET_KEY = 'your-secret-key'  # replace this in production

# ✅ Change this to False after verifying everything works
DEBUG = True

# Allow both local and EC2/S3 frontend URLs
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '54.235.61.181',  # your EC2 public IP
    'ai-course-coach-frontend.s3-website-us-east-1.amazonaws.com',  # your S3 frontend
]

# ----------------------------------------------------------------------
# APPS
# ----------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',  # must be above CommonMiddleware

    'api',
]

# ----------------------------------------------------------------------
# MIDDLEWARE
# ----------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',  # 👈 must be before CommonMiddleware

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ----------------------------------------------------------------------
# URL & WSGI
# ----------------------------------------------------------------------
ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# ----------------------------------------------------------------------
# DATABASE
# ----------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ----------------------------------------------------------------------
# PASSWORD VALIDATION
# ----------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------------------------------------------------------
# LANGUAGE / TIMEZONE
# ----------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------------------------
# STATIC FILES
# ----------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ----------------------------------------------------------------------
# CORS CONFIGURATION
# ----------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True  # ✅ Works for local & testing

# When ready for production (optional strict version):
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",  # local Vite dev
#     "http://127.0.0.1:5173",
#     "http://ai-course-coach-frontend.s3-website-us-east-1.amazonaws.com",
# ]

# ----------------------------------------------------------------------
# DEFAULT FIELD TYPE
# ----------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
