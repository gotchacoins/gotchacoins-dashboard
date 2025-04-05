from allauth.socialaccount.models import SocialLogin
from allauth.account.utils import perform_login
from allauth.account.models import EmailAddress
from allauth.account import app_settings
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy


from .forms import SocialSignupConsentForm  # 아래에 만들 예정
from .utils import generate_unique_username


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
            user.username = generate_unique_username(email=user.email)
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
            redirect_url=self.get_success_url(),
        )
