from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PortfolioSnapshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange_id = models.CharField(max_length=20)
    date = models.DateField()  # 일별 스냅샷
    cash_balance = models.FloatField()
    total_valuation = models.FloatField()
    total_buy_price = models.FloatField()
    profit = models.FloatField()
    profit_rate = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "exchange_id", "date")
        ordering = ["-date"]
        verbose_name = "포트폴리오 스냅샷"
        verbose_name_plural = "포트폴리오 스냅샷 목록"
