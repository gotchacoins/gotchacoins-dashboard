from django.urls import path
from .views import DashboardView, PortfolioView

app_name = "dashboard"
urlpatterns = [
    # path("settings/profile/"), # 프로필 수정
    # path("settings/exchange-keys/") 거래소 연동
    path("portfolio/<str:exchange_id>/", PortfolioView.as_view(), name="portfolio"),
    path("", DashboardView.as_view(), name="index"),
]
