from django.urls import path, include
from rest_framework import routers

from avanan.dpl import views

leak_router = routers.DefaultRouter()
leak_router.register(r'leak', views.APILeakViewSet, basename='dispositivo')

app_name = "leaks"

urlpatterns = [
    path(r'', include(leak_router.urls)),
]
