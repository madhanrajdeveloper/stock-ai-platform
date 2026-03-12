from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Prediction, PredictionQueue
from stocks.models import Stock

from .serializers import PredictionSerializer


@api_view(["POST"])
def add_to_prediction(request):

    symbol = request.data.get("symbol")

    stock = Stock.objects.filter(symbol=symbol).first()

    if not stock:
        return Response({"error": "stock not found"}, status=404)

    PredictionQueue.objects.create(stock=stock)

    return Response({"message": "added to prediction queue"})


@api_view(["GET"])
def get_predictions(request):

    predictions = Prediction.objects.all().order_by("-prediction_date")[:20]

    serializer = PredictionSerializer(predictions, many=True)

    return Response(serializer.data)