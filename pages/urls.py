from django.urls import path
from .views import HomePageView, AboutPageView, PrivacyPageView, TermsPageView

app_name = "pages"
urlpatterns = [
    path("privacy/", PrivacyPageView.as_view(), name="privacy"),
    path("terms/", TermsPageView.as_view(), name="terms"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("", HomePageView.as_view(), name="home"),
]
