from django.urls import path

from .views import (
    HomeView, AboutView, PricingView, ContactUs, PrivacyPolicyView,TermsAndConditionView
)

app_name = "website"
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('contact/', ContactUs.as_view(), name='contact'),

    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),

    path('terms-and-condition/', TermsAndConditionView.as_view(), name='terms-and-condition'),

]
