from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import CategoriaServico, Servico
from .serializers import CategoriaSimplesSerializer, CategoriaComServicosSerializer, ServicoSerializer
#view para serializers dinâmicos.
class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lista categorias.
    Padrão: Retorna apenas dados da categoria (Simples).
    Com filtro: ?include_servicos=true -> Retorna categoria E seus serviços.
    """
    queryset = CategoriaServico.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        include_servicos = self.request.query_params.get('include_servicos')

        if include_servicos == 'true':
            return CategoriaComServicosSerializer
        
        return CategoriaSimplesSerializer

class ServicoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [AllowAny]
