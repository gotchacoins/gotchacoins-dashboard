from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from allauth.account.forms import SignupForm
from django import forms

from .models import User


class UserCreationForm(DjangoUserCreationForm):

    class Meta:
        model = User
        fields = ("email", "username")


class UserChangeForm(DjangoUserChangeForm):

    class Meta:
        model = User
        fields = ("email", "username")


class SignupConsentForm(SignupForm):

    agree_terms = forms.BooleanField(
        label="이용약관에 동의합니다.",
        error_messages={"required": "이용약관에 동의해야 회원가입이 가능합니다."},
    )
    agree_privacy = forms.BooleanField(
        label="개인정보 처리방침에 동의합니다.",
        error_messages={
            "required": "개인정보 수집 및 이용에 동의해야 회원가입이 가능합니다."
        },
    )

    def save(self, request):
        user = super().save(request)
        return user


class SocialSignupConsentForm(forms.Form):
    agree_terms = forms.BooleanField(label="이용약관에 동의합니다.")
    agree_privacy = forms.BooleanField(label="개인정보 처리방침에 동의합니다.")
