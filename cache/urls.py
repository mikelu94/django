from django.urls import path

from . import views

urlpatterns = [
    path('get/<str:key>', views.cache_get),
    path('set/<str:key>', views.cache_set),
    path('del/<str:key>', views.cache_delete),
]
