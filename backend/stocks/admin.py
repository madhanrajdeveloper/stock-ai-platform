from django.contrib import admin
from .models import Stock, MarketData

admin.site.register(Stock)
admin.site.register(MarketData)