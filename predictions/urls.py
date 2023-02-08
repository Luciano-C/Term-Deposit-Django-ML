from django.urls import path
from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("read-more/", read_more, name="read_more")
]