from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from exchanges.context.portfolio import (
    get_portfolio_summary_context,
    get_portfolio_coins_context,
)


@login_required
def portfolio_coins_partial(request, exchange_id):
    context = get_portfolio_coins_context(request.user, exchange_id)

    html = render_to_string(
        "dashboard/partials/_portfolio_coins.html",
        {"holdings": context["holdings"]},  # 필요한 필드만 전달 가능
    )
    return HttpResponse(html)


@login_required
def portfolio_summary_partial(request, exchange_id):
    context = get_portfolio_summary_context(request.user, exchange_id)
    html = render_to_string(
        "dashboard/partials/_portfolio_summary.html", context, request=request
    )
    return HttpResponse(html)
