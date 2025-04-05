from django.urls import path
from .views import SocialConsentView

app_name = "accounts"
urlpatterns = [
    path("social/consent/", SocialConsentView.as_view(), name="social_consent"),
]
