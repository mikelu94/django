from django.http import HttpResponse

from .tasks import info_log


def index(request):
    info_log.delay('/task_queue was accessed')
    return HttpResponse('Task Queue')
