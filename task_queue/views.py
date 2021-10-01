from rest_framework.decorators import api_view
from rest_framework.response import Response

from .tasks import info_log

@api_view()
def index(request):
    info_log.delay('/task_queue was accessed')
    return Response('Task Queue')
