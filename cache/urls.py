from django.urls import path

from . import views

urlpatterns = [
    path('<str:key>', views.cache_view),
]
