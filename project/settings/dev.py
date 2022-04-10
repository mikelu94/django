import redis

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fake secret key for development purposes'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES['default']['HOST'] = 'postgres'

CACHES['default']['LOCATION'] = 'memcached:11211'

REDIS = redis.Redis(host='redis', port=6379, db=0)

CELERY_BROKER_URL = 'amqp://rabbitmq:5672'

LOGGING['handlers']['logstash']['host'] = 'logstash'
