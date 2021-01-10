from django.urls import path

from . import views

urlpatterns = [
    path('login', views.authn),
    path('login/redirect', views.user_data),
    path('logout', views.user_logout),
    path('oidc', views.root),
]