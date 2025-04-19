from django.urls import path
from dashboard.views import DashboardView, PortfolioView
from dashboard.partials.portfolio import (
    CoinsPartialView,
    SummaryPartialView,
)

app_name = "dashboard"
urlpatterns = [
    # 📊 대시보드
    path("", DashboardView.as_view(), name="index"),  # 전체 요약
    # path("insight/", InsightView.as_view(), name="insight"),  # 자산 분포 / 시장 지표
    # 📈 포트폴리오
    path("portfolio/<str:exchange_id>/", PortfolioView.as_view(), name="portfolio"),
    # path("analysis/holdings/", HoldingsAnalysisView.as_view(), name="analysis-holdings"),  # 보유 코인 분석
    # path("analysis/profit/", ProfitAnalysisView.as_view(), name="analysis-profit"),  # 수익률 분석
    # 📜 거래 내역
    # path("trades/", TradeHistoryView.as_view(), name="trades"),  # 체결 내역
    # path("transactions/", TransactionHistoryView.as_view(), name="transactions"),  # 입출금 내역
]

partial_urlpatterns = [
    path(
        "portfolio/<str:exchange_id>/coins/",
        CoinsPartialView.as_view(),
        name="portfolio-coins-partial",
    ),
    path(
        "portfolio/<str:exchange_id>/summary/",
        SummaryPartialView.as_view(),
        name="portfolio-summary-partial",
    ),
]

urlpatterns += partial_urlpatterns
