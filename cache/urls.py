from django.urls import path

from . import views

urlpatterns = [
    path('get/<str:key>', views.get),
    path('set/<str:key>', views.set),
    path('del/<str:key>', views.delete),
]
