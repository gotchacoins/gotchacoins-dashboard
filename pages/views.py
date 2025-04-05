from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class PrivacyPageView(TemplateView):
    template_name = "pages/privacy.html"


class TermsPageView(TemplateView):
    template_name = "pages/terms.html"
