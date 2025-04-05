from allauth.socialaccount.models import SocialLogin
from allauth.account.utils import perform_login
from allauth.account import app_settings
from allauth.account.models import EmailAddress
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
import uuid


# def terms_agreement(request):
#     if request.method == "POST":
#         serialized = request.session.pop("socialaccount_sociallogin", None)
#         if not serialized:
#             return redirect("account_login")

#         sociallogin = SocialLogin.deserialize(serialized)

#         if not sociallogin.user.username:
#             sociallogin.user.username = f"user_{uuid.uuid4().hex[:10]}"

#         print("[DEBUG] username:", sociallogin.user.username)
#         print("[DEBUG] email:", sociallogin.user.email)

#         user = sociallogin.user
#         user.set_unusable_password()
#         user.save()

#         # 이미 유저 저장했으므로 complete_social_login 호출 금지!
#         # 대신 소셜 계정만 연결 + 로그인만 처리

#         sociallogin.save(request, user)

#         # 이메일 주소 자동 등록
#         EmailAddress.objects.get_or_create(
#             user=user,
#             email=user.email,
#             defaults={"verified": True, "primary": True},
#         )

#         return perform_login(
#             request,
#             user,
#             email_verification=app_settings.EMAIL_VERIFICATION,
#         )

#     return render(request, "account/terms_agreement.html")

# accounts/views.py


from .forms import SocialSignupConsentForm  # 아래에 만들 예정


class SocialConsentView(FormView):
    template_name = "account/social_consent.html"
    form_class = SocialSignupConsentForm
    success_url = reverse_lazy("pages:home")

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("socialaccount_sociallogin"):
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        serialized = self.request.session.pop("socialaccount_sociallogin", None)
        if not serialized:
            return redirect("account_login")

        sociallogin = SocialLogin.deserialize(serialized)
        user = sociallogin.user

        if not user.username:
            user.username = f"user_{uuid.uuid4().hex[:10]}"
        user.set_unusable_password()
        user.save()

        # 연결된 소셜 계정 저장
        sociallogin.save(self.request, user)

        # 이메일 인증 등록
        EmailAddress.objects.get_or_create(
            user=user,
            email=user.email,
            defaults={"verified": True, "primary": True},
        )

        return perform_login(
            self.request,
            user,
            email_verification=app_settings.EMAIL_VERIFICATION,
        )
