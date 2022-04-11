import redis

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g-2c^+c++d$17y-9ir+0o4-tf3%5du2v2ah&=#b85@5mlb19+_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES['default']['HOST'] = os.getenv('POSTGRES_SVC')

CACHES['default']['LOCATION'] = f"{os.getenv('MEMCACHED_SVC')}:11211"

REDIS = redis.Redis(host=os.getenv('REDIS_SVC'), port=6379, db=0)

CELERY_BROKER_URL = f"amqp://{os.getenv('RABBITMQ_SVC')}:5672"

LOGGING['handlers']['logstash']['host'] = os.getenv('LOGSTASH_SVC')
LOGGING['handlers']['logstash']['port'] = int(os.getenv('LOGSTASH_PORT'))

STATIC_ROOT = '/static'
STATIC_URL = 'static/'
