from rest_framework import serializers
from .models import Prediction


class PredictionSerializer(serializers.ModelSerializer):

    symbol = serializers.CharField(source="stock.symbol")

    class Meta:
        model = Prediction
        fields = [
            "id",
            "symbol",
            "predicted_close",
            "prediction_type",
            "confidence",
            "prediction_date",
        ]