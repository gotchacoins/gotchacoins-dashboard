from django.urls import path
from .views import DashboardView, PortfolioView
from .partial_views.portfolio import portfolio_coins_partial, portfolio_summary_partial

app_name = "dashboard"
urlpatterns = [
    # path("settings/profile/"), # 프로필 수정
    # path("settings/exchange-keys/") 거래소 연동
    path("portfolio/<str:exchange_id>/", PortfolioView.as_view(), name="portfolio"),
    path("", DashboardView.as_view(), name="index"),
]

partial_urlpatterns = [
    path(
        "portfolio/<str:exchange_id>/items/",
        portfolio_coins_partial,
        name="portfolio-coins-partial",
    ),
    path(
        "portfolio/<str:exchange_id>/summary/",
        portfolio_summary_partial,
        name="portfolio-summary-partial",
    ),
]

urlpatterns += partial_urlpatterns
