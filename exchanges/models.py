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

    class Meta:
        verbose_name = "거래소"
        verbose_name_plural = "거래소 목록"


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

        verbose_name = "거래쌍"
        verbose_name_plural = "거래쌍 목록"


class UserExchangeKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)

    access_key = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=200)

    # 사용자 구분용 라벨 (예: "내 업비트 계정")
    label = models.CharField(max_length=50, blank=True)

    is_active = models.BooleanField(default=True)  # 사용 여부
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.exchange.id}"

    class Meta:
        unique_together = ("user", "exchange")

        verbose_name = "거래소 API 키"
        verbose_name_plural = "거래소 API 키 목록"


class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)

    market = models.CharField(max_length=30)  # 예: KRW-BTC (마켓 코드)
    currency = models.CharField(max_length=10)  # 예: BTC, ETH

    balance = models.DecimalField(max_digits=20, decimal_places=8)  # 주문 가능 수량
    locked = models.DecimalField(max_digits=20, decimal_places=8)  # 주문 중인 수량
    avg_buy_price = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # 매수 평균 단가

    unit_currency = models.CharField(max_length=10)  # 기준 화폐 단위 (예: KRW, BTC 등)

    # evaluated_price, profit, profit_rate 등은 Redis에서 실시간 가격으로 계산

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "exchange", "currency")
        indexes = [
            models.Index(fields=["user", "exchange"]),  # 자산 조회용
            models.Index(
                fields=["user", "exchange", "currency"]
            ),  # 보유 자산 단일 조회용
            models.Index(fields=["market"]),  # 시장 코드 기준 조회
        ]

        verbose_name = "보유 자산"
        verbose_name_plural = "보유 자산 목록"

    def __str__(self):
        return f"{self.user} {self.exchange} {self.currency}"
