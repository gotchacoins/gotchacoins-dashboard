from django.urls import path
from .views import DashboardView

app_name = "dashboard"
urlpatterns = [
    # path("portfolio/upbit/"),
    # path("portfolio/bithumb/"),
    path("", DashboardView.as_view(), name="index"),
]
