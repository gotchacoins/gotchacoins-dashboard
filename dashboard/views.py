from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from exchanges.context.portfolio import (
    get_portfolio_summary_context,
    get_portfolio_coins_context,
)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"


class PortfolioView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/portfolio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exchange_id = self.kwargs.get("exchange_id")
        page = int(self.request.GET.get("page", 1))
        limit = int(self.request.GET.get("limit", 20))

        context.update(get_portfolio_summary_context(self.request.user, exchange_id))
        context.update(
            get_portfolio_coins_context(self.request.user, exchange_id, page, limit)
        )
        return context
