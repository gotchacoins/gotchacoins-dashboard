from django.contrib import admin

from .models import PortfolioSnapshot


@admin.register(PortfolioSnapshot)
class PortfolioSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "exchange_id",
        "date",
        "cash_balance",
        "total_valuation",
        "total_buy_price",
        "profit",
        "profit_rate",
    )
