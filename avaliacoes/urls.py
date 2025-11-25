from django.urls import path
from .views import CriarAvaliacaoView

urlpatterns = [
    path('', CriarAvaliacaoView.as_view(), name='criar-avaliacao'),
]
