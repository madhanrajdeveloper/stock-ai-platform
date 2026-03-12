from django.db import models


class Stock(models.Model):

    symbol = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    exchange = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symbol


class MarketData(models.Model):

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()

    volume = models.BigIntegerField()

    date = models.DateField()

    class Meta:
        unique_together = ("stock", "date")

    def __str__(self):
        return f"{self.stock.symbol} - {self.date}"