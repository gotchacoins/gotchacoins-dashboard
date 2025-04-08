from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


from exchanges.models import UserExchangeKey
from exchanges.clients.upbit import UpbitClient


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"


# dashboard/views/portfolio.py


class PortfolioView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/portfolio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exchange_id = self.kwargs.get("exchange_id")

        try:
            key = UserExchangeKey.objects.get(
                user=self.request.user, exchange__id=exchange_id
            )
            if exchange_id == "upbit":

                client = UpbitClient(key.access_key, key.secret_key)
                holdings = client.get_holdings()
            else:
                context["error_message"] = (
                    f"[{exchange_id}] 아직 지원되지 않는 거래소입니다."
                )
                return context

            if isinstance(holdings, dict) and holdings.get("error"):
                context["error_message"] = holdings["message"]
                context["holdings"] = []
            else:
                context["holdings"] = holdings

        except UserExchangeKey.DoesNotExist:
            context["error_message"] = (
                f"{exchange_id.upper()} API 키가 등록되어 있지 않습니다."
            )
            context["holdings"] = []

        context["exchange_id"] = exchange_id
        return context
