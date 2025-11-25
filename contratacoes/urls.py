from django.urls import path
from .views import IniciarContatoWhatsAppView

urlpatterns = [
    path('iniciar/', IniciarContatoWhatsAppView.as_view(), name='iniciar-contato-whatsapp'),
]
