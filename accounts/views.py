from allauth.socialaccount.models import SocialLogin
from allauth.account.utils import perform_login
from allauth.account.models import EmailAddress
from allauth.account import app_settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib import messages
import requests
from django.core.files.base import ContentFile

from .mixins import SocialSessionRequiredMixin
from .forms import SocialSignupConsentForm, ProfileEditForm
from .utils import generate_unique_username
from .helpers import get_name_and_avatar

User = get_user_model()


class SocialConsentView(SocialSessionRequiredMixin, FormView):
    template_name = "account/social_consent.html"
    form_class = SocialSignupConsentForm
    success_url = reverse_lazy("dashboard:index")

    def form_valid(self, form):
        serialized = self.request.session.pop("socialaccount_sociallogin", None)
        if not serialized:
            return redirect("account_login")

        sociallogin = SocialLogin.deserialize(serialized)
        user = sociallogin.user

        with transaction.atomic():

            # 이름, 아바타 설정
            provider = sociallogin.account.provider
            extra_data = sociallogin.account.extra_data
            first_name, last_name, avatar_url = get_name_and_avatar(
                provider, extra_data
            )

            user.first_name = first_name or user.first_name
            user.last_name = last_name or user.last_name
            # user.avatar_url = avatar_url or user.avatar_url
            user.username = user.username or generate_unique_username(email=user.email)
            user.set_unusable_password()

            # ✅ avatar_url을 ImageField에 저장하기
            if avatar_url and not user.avatar:
                try:
                    response = requests.get(avatar_url)
                    if response.status_code == 200:
                        user.avatar.save(
                            f"{user.username}_avatar.jpg",
                            ContentFile(response.content),
                            save=False,
                        )
                except Exception as e:
                    print("❗ 소셜 아바타 다운로드 실패:", e)

            user.save()

            form.save(user)  # 약관 저장

            sociallogin.save(self.request, user)

            EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                defaults={"verified": True, "primary": True},
            )

        return perform_login(
            self.request,
            user,
            email_verification=app_settings.EMAIL_VERIFICATION,
            redirect_url=self.get_success_url(),
        )

    def get_success_url(self):
        return self.request.GET.get("next") or self.success_url


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = "account/profile_edit.html"
    success_url = reverse_lazy("accounts:profile_edit")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        # 프로필 수정 후 메시지 추가
        response = super().form_valid(form)
        messages.success(self.request, "Your profile has been updated successfully!")
        return response
