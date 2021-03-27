from .base import *
import redis

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fake secret key for development purposes'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES['default']['NAME'] = 'django'
DATABASES['default']['USER'] = 'user'
DATABASES['default']['PASSWORD'] = 'password'
DATABASES['default']['HOST'] = 'postgres'

CACHES['default']['LOCATION'] = 'memcached:11211'

REDIS = redis.Redis(host='redis', port=6379, db=0)

CELERY_BROKER_URL = 'amqp://rabbitmq:5672'

KAFKA_SERVERS = ['kafka:9092']

LOGGING['handlers']['logstash']['host'] = 'logstash'
