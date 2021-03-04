from django.urls import path
from .webhooks import webhook

urlpatterns = [
    path('', webhook, name='webhook'),
]