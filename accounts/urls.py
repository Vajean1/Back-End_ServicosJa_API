from django.urls import path
from .views import ClienteRegistrationView, PrestadorRegistrationView, PrestadorListView, PrestadorProfileEditView

urlpatterns = [
    #Urls de cadastro
    path('registro/cliente/', ClienteRegistrationView.as_view(), name='registrar-cliente'),
    path('registro/prestador/', PrestadorRegistrationView.as_view(), name='registrar-prestador'),

    #Urls de filtro público
    path('prestadores/', PrestadorListView.as_view(), name='lista-prestadores'),

    # Urls autenticadas
    path('perfil/prestador/editar/', PrestadorProfileEditView.as_view(), name='editar-perfil-prestador'),
]
