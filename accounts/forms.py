from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from allauth.account.forms import SignupForm
from django.conf import settings
from django.db import transaction
from django import forms

from .models import User, UserAgreement, AgreementType


AGREEMENT_VERSION = getattr(settings, "AGREEMENT_VERSION", "1.0")


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
    agree_marketing = forms.BooleanField(
        label="이벤트 및 혜택 알림 수신에 동의합니다.",
        required=False,
        error_messages={"required": "이벤트 및 혜택 알림 수신 여부를 선택해주세요."},
    )

    def save(self, request):
        with transaction.atomic():
            user = super().save(request)

            agreements = [
                UserAgreement(
                    user=user,
                    agreement_type=AgreementType.TERMS,
                    agreed=True,
                    version=AGREEMENT_VERSION,
                ),
                UserAgreement(
                    user=user,
                    agreement_type=AgreementType.PRIVACY,
                    agreed=True,
                    version=AGREEMENT_VERSION,
                ),
            ]

            if self.cleaned_data.get("agree_marketing"):
                agreements.append(
                    UserAgreement(
                        user=user,
                        agreement_type=AgreementType.MARKETING,
                        agreed=True,
                        version=AGREEMENT_VERSION,
                    )
                )

            UserAgreement.objects.bulk_create(agreements)

            return user


class SocialSignupConsentForm(forms.Form):
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
    agree_marketing = forms.BooleanField(
        label="이벤트 및 혜택 알림 수신에 동의합니다.",
        required=False,
        error_messages={"required": "이벤트 및 혜택 알림 수신 여부를 선택해주세요."},
    )

    def save(self, user):
        with transaction.atomic():
            agreements = [
                UserAgreement(
                    user=user,
                    agreement_type=AgreementType.TERMS,
                    agreed=True,
                    version=AGREEMENT_VERSION,
                ),
                UserAgreement(
                    user=user,
                    agreement_type=AgreementType.PRIVACY,
                    agreed=True,
                    version=AGREEMENT_VERSION,
                ),
            ]

            if self.cleaned_data.get("agree_marketing"):
                agreements.append(
                    UserAgreement(
                        user=user,
                        agreement_type=AgreementType.MARKETING,
                        agreed=True,
                        version=AGREEMENT_VERSION,
                    )
                )

            UserAgreement.objects.bulk_create(agreements)


class ProfileEditForm(forms.ModelForm):

    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "class": "hidden",
                "id": "avatar-upload",
                "accept": "image/*",
                "onchange": "previewImage(event)",
            }
        )
    )

    class Meta:
        model = User
        fields = ["first_name", "avatar"]
