from rest_framework import generics, permissions
from .models import Avaliacao
from .serializers import CriarAvaliacaoSerializer

class CriarAvaliacaoView(generics.CreateAPIView):
    """
    Endpoint para criar uma avaliação.
    O usuário precisa estar logado
    """
    queryset = Avaliacao.objects.all()
    serializer_class = CriarAvaliacaoSerializer
    permission_classes = [permissions.IsAuthenticated]