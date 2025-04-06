from django.urls import path
from .views import SocialConsentView, ProfileEditView

app_name = "accounts"
urlpatterns = [
    path("social/consent/", SocialConsentView.as_view(), name="social_consent"),
    path("profile/", ProfileEditView.as_view(), name="profile_edit"),
]
