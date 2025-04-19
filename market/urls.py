from django.urls import path

app_name = "market"
urlpatterns = [
    # path("market/price/", MarketPriceView.as_view(), name="market-price"), # 실시간 시세
    # path("market/trending/", MarketTrendingView.as_view(), name="market-trending"), # 트렌드 코인
    # path("market/daily-change/", MarketDailyChangeView.as_view(), name="market-daily-change"), # 일간 변동률
    # path("market/volume-surge/", MarketVolumeSurgeView.as_view(), name="market-volume-surge"), # 거래량 급등 코인
]
