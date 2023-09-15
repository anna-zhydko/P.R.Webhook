import sys
from urllib.parse import urlparse

from django.apps import AppConfig
from django.conf import settings


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"
    verbose_name = "main"
