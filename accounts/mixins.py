from django.shortcuts import redirect


class SocialSessionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("socialaccount_sociallogin"):
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)
