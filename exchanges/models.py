from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Exchange(models.Model):
    id = models.CharField(max_length=20, primary_key=True)  # 예: "upbit", "bithumb"
    name = models.CharField(max_length=50)  # 예: "업비트"
    base_url = models.URLField(blank=True)  # ex: https://api.upbit.com
    logo_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Market(models.Model):
    exchange = models.ForeignKey(
        Exchange, on_delete=models.CASCADE, related_name="markets"
    )
    market = models.CharField(max_length=30)  # 예: KRW-BTC
    base_currency = models.CharField(max_length=10)
    quote_currency = models.CharField(max_length=10)

    korean_name = models.CharField(max_length=50)
    english_name = models.CharField(max_length=50)
    market_warning = models.CharField(max_length=20, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("exchange", "market")
        indexes = [
            models.Index(fields=["exchange", "base_currency"]),
            models.Index(fields=["base_currency"]),
            models.Index(fields=["market"]),
        ]


class UserExchangeKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)

    access_key = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=200)

    # 사용자 구분용 라벨 (예: "내 업비트 계정")
    label = models.CharField(max_length=50, blank=True)

    is_active = models.BooleanField(default=True)  # 사용 여부
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "exchange")

    def __str__(self):
        return f"{self.user} - {self.exchange.id}"
