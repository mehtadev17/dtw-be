from django.conf.urls import include
from django.urls import path
from api.router import router

urlpatterns = [
    path('', include(router.urls))
]
