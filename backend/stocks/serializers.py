from rest_framework import serializers
from .models import Stock, MarketData


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = "__all__"


class MarketDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarketData
        fields = "__all__"