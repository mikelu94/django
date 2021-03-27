from .base import *
import redis

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g-2c^+c++d$17y-9ir+0o4-tf3%5du2v2ah&=#b85@5mlb19+_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES['default']['NAME'] = 'django'
DATABASES['default']['USER'] = 'django_user'
DATABASES['default']['PASSWORD'] = 'password'
DATABASES['default']['HOST'] = '127.0.0.1'

CACHES['default']['LOCATION'] = '127.0.0.1:11211'

REDIS = redis.Redis(host='127.0.0.1', port=6379, db=0)

CELERY_BROKER_URL = 'amqp://127.0.0.1:5672'

KAFKA_SERVERS = ['127.0.0.1:9092']

LOGGING['handlers']['logstash']['host'] = '127.0.0.1'

STATIC_ROOT = '/static'
