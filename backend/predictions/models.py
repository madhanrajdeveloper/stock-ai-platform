from django.db import models
from stocks.models import Stock


class Prediction(models.Model):

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    predicted_close = models.FloatField()

    prediction_type = models.CharField(max_length=50)

    confidence = models.FloatField()

    prediction_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock.symbol} | {self.prediction_type}"


class PredictionQueue(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed")
    ]

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock.symbol} - {self.status}"