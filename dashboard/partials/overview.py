from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from dashboard.contexts.overview import get_dashboard_summary_context

from common.utils.cache import get_or_set_cache


class DashboardSummaryPartialView(APIView):

    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dashboard/partials/_dashboard_summary.html"

    def get(self, request):

        context = get_or_set_cache(
            key=f"portfolio:{request.user.id}:dashboard:summary",
            ttl=3,
            compute_fn=lambda: get_dashboard_summary_context(request.user),
        )

        return Response(context)
