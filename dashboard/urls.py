from django.urls import path
from .views import DashboardView, PortfolioView

app_name = "dashboard"
urlpatterns = [
    path("portfolio/<str:exchange_id>/", PortfolioView.as_view(), name="portfolio"),
    path("", DashboardView.as_view(), name="index"),
]
