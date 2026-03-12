from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Stock, MarketData
from .serializers import StockSerializer, MarketDataSerializer


@api_view(["GET"])
def search_stock(request):

    query = request.GET.get("q", "")

    stocks = Stock.objects.filter(symbol__icontains=query)[:10]

    serializer = StockSerializer(stocks, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def chart_data(request):

    symbol = request.GET.get("symbol")

    stock = Stock.objects.filter(symbol=symbol).first()

    if not stock:
        return Response({"error": "stock not found"}, status=404)

    data = MarketData.objects.filter(stock=stock).order_by("date")

    serializer = MarketDataSerializer(data, many=True)

    return Response(serializer.data)