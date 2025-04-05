# accounts/adapters.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, perform_login
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if request.user.is_authenticated:
            return

        email = user_email(sociallogin.user)
        if not email:
            return

        try:
            existing_user = User.objects.get(email=email)
        except User.DoesNotExist:
            return  # 신규 유저는 allauth가 처리

        # 연결 및 로그인 처리
        sociallogin.connect(request, existing_user)
        raise ImmediateHttpResponse(
            perform_login(request, existing_user, email_verification="optional")
        )
