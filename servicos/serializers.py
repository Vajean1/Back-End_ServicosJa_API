from rest_framework import serializers
from .models import CategoriaServico, Servico

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ['id', 'nome', 'descricao']
#Apenas categorias
class CategoriaSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaServico
        fields = ['id', 'nome', 'descricao', 'icone']
#Categorias + servicos
class CategoriaComServicosSerializer(serializers.ModelSerializer):
    servicos = ServicoSerializer(many=True, read_only=True)

    class Meta:
        model = CategoriaServico
        fields = ['id', 'nome', 'descricao', 'icone', 'servicos']