from django.contrib.auth.models import AbstractUser
from django.db import models

from common.utils.storage import get_public_storage


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to="avatars/", storage=get_public_storage(), blank=True, null=True
    )

    def __str__(self):
        return self.email


class AgreementType(models.TextChoices):
    TERMS = "terms", "이용약관"
    PRIVACY = "privacy", "개인정보 처리방침"
    MARKETING = "marketing", "마케팅 수신 동의"


class UserAgreement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agreement_type = models.CharField(max_length=20, choices=AgreementType.choices)
    agreed = models.BooleanField(default=True)
    agreed_at = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=10, default="1.0")

    class Meta:
        unique_together = ("user", "agreement_type", "version")

    def __str__(self):
        status = "✅" if self.agreed else "❌"
        return f"{self.user} | {self.agreement_type}:{status} v{self.version}"
