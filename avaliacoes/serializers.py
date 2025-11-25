from rest_framework import serializers
from .models import Avaliacao
from contratacoes.models import SolicitacaoContato

class CriarAvaliacaoSerializer(serializers.ModelSerializer):
    # O cliente envia o ID da solicitação de contato que quer avaliar
    solicitacao_contato_id = serializers.PrimaryKeyRelatedField(
        queryset=SolicitacaoContato.objects.all(),
        source='solicitacao_contato'
    )

    class Meta:
        model = Avaliacao
        fields = ['solicitacao_contato_id', 'nota', 'comentario']

    def validate_solicitacao_contato_id(self, value):
        # Verifica se a solicitação pertence ao usuário logado
        user = self.context['request'].user
        
        if value.cliente != user:
            raise serializers.ValidationError("Você só pode avaliar contatos que você iniciou.")
        
        return value