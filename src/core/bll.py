from .models import Application
from django.utils.text import slugify


def get_or_create_application():
    applications = Application.objects.all()
    return applications[0] if applications else Application.objects.create()
