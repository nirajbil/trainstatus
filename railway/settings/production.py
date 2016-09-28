import os
from django.conf import settings


DEBUG = False
TEMPLATE_DEBUG = True

DATABASES = settings.DATABASES

# parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()

#Honor  the "X-FORWARDED-Proto" header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO','https')

#allow all host header
ALLOWED_HOSTS = ['*']

#static asset configuration
#import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = "staticfiles"
STATIC_URL = "/static/"

STATICFILES_DIRS = {
    os.path.join(BASE_DIR,'static'),
}



