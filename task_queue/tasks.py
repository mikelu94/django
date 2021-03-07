from celery import shared_task
from time import sleep


@shared_task
def info_log(message):
    sleep(60)
    print(message)
