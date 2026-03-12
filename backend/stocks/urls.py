from django.urls import path
from .views import search_stock, chart_data

urlpatterns = [
    path("search", search_stock),
    path("chart-data", chart_data),
]