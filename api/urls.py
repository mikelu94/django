from django.urls import path

from . import views

urlpatterns = [
    path('set', views.SetView.as_view(), name='set'),
    path('set/<uuid:uuid>', views.SetView.as_view(), name='set'),
    path('element', views.ElementView.as_view(), name='element'),
    path('element/<uuid:uuid>', views.ElementView.as_view(), name='element'),
]
