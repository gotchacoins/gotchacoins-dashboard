from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


from exchanges.models import UserExchangeKey
from exchanges.clients.upbit import UpbitClient


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"


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


# class ProfileSettingsView(LoginRequiredMixin, TemplateView):
#     template_name = "dashboard/settings/profile.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["profile_form"] = ProfileForm(instance=self.request.user)
#         context["notification_form"] = NotificationForm(instance=self.request.user.profile)
#         context["time_form"] = TimezoneForm(instance=self.request.user.profile)
#         return context

#     def post(self, request, *args, **kwargs):
#         profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)
#         notification_form = NotificationForm(request.POST, instance=request.user.profile)
#         time_form = TimezoneForm(request.POST, instance=request.user.profile)

#         if all([profile_form.is_valid(), notification_form.is_valid(), time_form.is_valid()]):
#             profile_form.save()
#             notification_form.save()
#             time_form.save()
#             messages.success(request, "프로필이 업데이트되었습니다.")
#             return redirect("dashboard:settings_profile")

#         context = self.get_context_data()
#         context.update({
#             "profile_form": profile_form,
#             "notification_form": notification_form,
#             "time_form": time_form,
#         })
#         return self.render_to_response(context)
