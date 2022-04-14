import redis

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES['default']['HOST'] = 'postgres'

CACHES['default']['LOCATION'] = 'memcached:11211'

REDIS = redis.Redis(host='redis', port=6379, db=0)

CELERY_BROKER_URL = 'amqp://rabbitmq:5672'

LOGGING['handlers']['logstash']['host'] = 'logstash'
LOGGING['handlers']['logstash']['port'] = 5959
