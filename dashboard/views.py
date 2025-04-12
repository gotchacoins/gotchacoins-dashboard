from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from exchanges.services.portfolio import get_portfolio_context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"


class PortfolioView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/portfolio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exchange_id = self.kwargs.get("exchange_id")
        context.update(get_portfolio_context(self.request.user, exchange_id))
        return context
