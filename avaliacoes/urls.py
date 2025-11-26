from django.urls import path
from .views import CriarAvaliacaoView, AvaliacaoListView, AvaliacaoDetailView

urlpatterns = [
    path('', CriarAvaliacaoView.as_view(), name='criar-avaliacao'),
    path('listar/', AvaliacaoListView.as_view(), name='listar-avaliacoes'),
    path('<int:pk>/', AvaliacaoDetailView.as_view(), name='detalhe-avaliacao'),
]
