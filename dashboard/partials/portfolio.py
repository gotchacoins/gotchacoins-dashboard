from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from dashboard.contexts.portfolio import (
    get_portfolio_coins_context,
    get_portfolio_summary_context,
)

from common.utils.cache import get_or_set_cache


class PortfolioCoinsPartialView(APIView):

    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dashboard/partials/_portfolio_coins.html"

    def get(self, request, exchange_id):

        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 20))

        context = get_or_set_cache(
            key=f"portfolio:{request.user.id}:{exchange_id}:portfolio:coins",
            ttl=3,
            compute_fn=lambda: get_portfolio_coins_context(
                request.user, exchange_id, page, limit
            ),
        )

        return Response(context)


class PortfolioSummaryPartialView(APIView):

    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dashboard/partials/_portfolio_summary.html"

    def get(self, request, exchange_id):

        context = get_or_set_cache(
            key=f"portfolio:{request.user.id}:{exchange_id}:portfolio:summary",
            ttl=3,
            compute_fn=lambda: get_portfolio_summary_context(request.user, exchange_id),
        )

        return Response(context)
