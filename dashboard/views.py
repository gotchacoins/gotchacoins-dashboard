from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from exchanges.context.portfolio import (
    get_portfolio_summary_context,
    get_portfolio_coins_context,
)


class DashboardView(APIView):

    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "dashboard/index.html"

    def get(self, request):
        return Response({})


class PortfolioView(APIView):

    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "dashboard/portfolio.html"

    def get(self, request, exchange_id):

        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 20))

        coins_context = get_portfolio_coins_context(
            request.user, exchange_id, page, limit
        )
        summary_context = get_portfolio_summary_context(request.user, exchange_id)

        context = coins_context | summary_context

        return Response(context)
