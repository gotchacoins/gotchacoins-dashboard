# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from exchanges.services.portfolio import get_portfolio_context


# class PortfolioView(LoginRequiredMixin, TemplateView):
#     template_name = "dashboard/portfolio.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         exchange_id = self.kwargs.get("exchange_id")
#         context.update(get_portfolio_context(self.request.user, exchange_id))
#         context["exchange_id"] = exchange_id
#         return context


@login_required
def portfolio_coins_partial(request, exchange_id):
    context = get_portfolio_context(request.user, exchange_id)

    html = render_to_string(
        "dashboard/partials/_portfolio_coins.html",
        {"holdings": context["holdings"]},  # 필요한 필드만 전달 가능
    )
    return HttpResponse(html)


@login_required
def portfolio_summary_partial(request, exchange_id):
    context = get_portfolio_context(request.user, exchange_id)
    html = render_to_string(
        "dashboard/partials/_portfolio_summary.html", context, request=request
    )
    return HttpResponse(html)
