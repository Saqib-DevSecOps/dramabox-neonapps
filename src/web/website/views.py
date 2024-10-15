from django.shortcuts import render
from django.views.generic import TemplateView

from src.apps.whisper.main import NotificationService
from src.services.drama.models import DramaSeries, Testimonials


# Create your views here.
class HomeView(TemplateView):
    template_name = 'website/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        drama_series_list = DramaSeries.objects.all()

        context['currently_featured'] = [series for series in drama_series_list if series.is_currently_featured][:10]
        context['trending_series'] = [series for series in drama_series_list if series.is_trending][:10]
        context['upcoming_series'] = [series for series in drama_series_list if series.upcoming_series] [:10]
        context['top_three_series'] = DramaSeries.objects.order_by('-view_count')[:3]
        context['testimonials'] = Testimonials.objects.all().order_by('-created_at')[:5]
        return context

class AboutView(TemplateView):
    template_name = 'website/about.html'

class PricingView(TemplateView):
    template_name = 'website/pricing.html'

class ContactUs(TemplateView):
    template_name = 'website/contact.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'website/privacy_policy.html'

class TermsAndConditionView(TemplateView):
    template_name = 'website/terms_and_condition.html'