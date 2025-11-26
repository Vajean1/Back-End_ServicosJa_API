from rest_framework import generics, permissions
from .models import Avaliacao
from .serializers import CriarAvaliacaoSerializer, AvaliacaoSerializer

class CriarAvaliacaoView(generics.CreateAPIView):
    """
    Endpoint para criar uma avaliação.
    O usuário precisa estar logado
    """
    queryset = Avaliacao.objects.all()
    serializer_class = CriarAvaliacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

class AvaliacaoListView(generics.ListAPIView):
    """
    Lista avaliações. Permite filtrar por prestador (user ID).
    """
    serializer_class = AvaliacaoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Avaliacao.objects.all()
        prestador_id = self.request.query_params.get('prestador')
        
        if prestador_id:
            queryset = queryset.filter(solicitacao_contato__prestador__id=prestador_id)
            
        return queryset

class AvaliacaoDetailView(generics.RetrieveAPIView):
    """
    Recupera uma avaliação específica pelo ID.
    """
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    permission_classes = [permissions.AllowAny]
