from django.urls import path
from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("read-more/", read_more, name="read_more"),
    path("signin/", signin, name="signin"),
    path("signup/", signup, name="signup"),
    path("signout/", signout, name="signout"),
    path("predictions/", predictions, name="predictions")
]