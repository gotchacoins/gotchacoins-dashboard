from django.contrib import admin
from .models import (
    Exchange,
    UserExchangeKey,
    Market,
)


# Register your models here.
@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    pass


@admin.register(UserExchangeKey)
class UserExchangeKeyAdmin(admin.ModelAdmin):
    pass


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    pass
