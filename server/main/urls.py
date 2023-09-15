from django.urls import path

from . import views

urlpatterns = [
    path('', views.handle_webhook_event, name='handle_webhook_event'),
]
