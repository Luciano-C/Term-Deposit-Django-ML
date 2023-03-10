from django.urls import path
from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("read-more/", read_more, name="read_more"),
    path("signin/", signin, name="signin"),
    path("signup/", signup, name="signup"),
    path("signout/", signout, name="signout"),
    path("predictions/", predictions, name="predictions"),
    path("single_prediction/", single_prediction, name="single_prediction"),
    path("multiple_predictions/", multiple_predictions, name="multiple_predictions"),
    path("my_predictions/", my_predictions, name="my_predictions"),
    path("manage_client/<int:client_id>", manage_client, name="manage_client"),
    path("search_clients/", search_clients, name="search_clients"),
    path("charts/", charts, name="charts")
]