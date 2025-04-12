from django.contrib import admin
from .models import (
    Exchange,
    UserExchangeKey,
    Market,
    Holding,
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
    list_display = (
        "exchange",  # 거래소 (예: 업비트)
        "market",  # 마켓 코드 (KRW-BTC)
        "korean_name",  # 한글 이름
        "english_name",  # 영어 이름
        "base_currency",  # 코인
        "quote_currency",  # 기준 화폐
        "market_warning",  # 유의 종목 여부
        "updated_at",  # 마지막 업데이트
    )
    list_filter = ("exchange", "quote_currency", "market_warning")  # 사이드 필터
    search_fields = ("market", "korean_name", "english_name")  # 상단 검색창
    ordering = ("exchange", "market")  # 기본 정렬
    list_per_page = 50  # 페이지당 항목 수

    readonly_fields = ("updated_at",)  # 수정 금지 필드


@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    pass
