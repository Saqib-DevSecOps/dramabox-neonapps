from django.urls import path

from .views import (
    HomeView, AboutView, PricingView, ContactUs
)

app_name = "website"
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('contact/', ContactUs.as_view(), name='contact'),

]
