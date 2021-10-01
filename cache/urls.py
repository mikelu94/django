from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('<str:key>', csrf_exempt(views.CacheView.as_view())),
]
