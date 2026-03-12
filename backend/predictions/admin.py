from django.contrib import admin
from .models import Prediction, PredictionQueue

admin.site.register(Prediction)
admin.site.register(PredictionQueue)