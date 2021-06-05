from time import sleep

from celery import shared_task


@shared_task
def info_log(message):
    sleep(60)
    print(message)
