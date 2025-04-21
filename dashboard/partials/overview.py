from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from dashboard.contexts.overview import get_dashboard_summary_context
from dashboard.services.portfolio import save_portfolio_snapshot


class DashboardSummaryPartialView(APIView):

    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dashboard/partials/_dashboard_summary.html"

    def get(self, request):

        context = get_dashboard_summary_context(request.user)

        save_portfolio_snapshot(request.user, exchange_id=None)

        return Response(context)
