from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'sets', views.SetViewSet)
router.register(r'elements', views.ElementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
