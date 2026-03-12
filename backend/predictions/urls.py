from django.urls import path
from .views import add_to_prediction, get_predictions

urlpatterns = [
    path("add", add_to_prediction),
    path("", get_predictions),
]