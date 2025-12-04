from rest_framework import serializers
from .models import Avaliacao
from contratacoes.models import SolicitacaoContato

class CriarAvaliacaoSerializer(serializers.ModelSerializer):
    solicitacao_contato_id = serializers.PrimaryKeyRelatedField(
        queryset=SolicitacaoContato.objects.all(),
        source='solicitacao_contato'
    )

    class Meta:
        model = Avaliacao
        fields = ['solicitacao_contato_id', 'nota', 'comentario']

    def validate_solicitacao_contato_id(self, value):
        user = self.context['request'].user
        
        if value.cliente != user:
            raise serializers.ValidationError("Você só pode avaliar contatos que você iniciou.")
        
        if not value.servico_realizado:
            raise serializers.ValidationError("Este serviço ainda não foi marcado como concluído pelo prestador.")

        if hasattr(value, 'avaliacao'):
             raise serializers.ValidationError("Este serviço já foi avaliado.")

        return value

class AvaliacaoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='solicitacao_contato.cliente.nome_completo', read_only=True)
    prestador_nome = serializers.CharField(source='solicitacao_contato.prestador.nome_completo', read_only=True)
    prestador_id = serializers.IntegerField(source='solicitacao_contato.prestador.id', read_only=True)
    prestador_foto = serializers.SerializerMethodField()
    data = serializers.DateTimeField(source='data_criacao', format="%d/%m/%Y", read_only=True)
    
    class Meta:
        model = Avaliacao
        fields = ['id', 'cliente_nome', 'prestador_nome', 'prestador_id', 'prestador_foto', 'nota', 'comentario', 'data']

    def get_prestador_foto(self, obj):
        try:
            profile = obj.solicitacao_contato.prestador.perfil_prestador
            if profile.foto_perfil:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(profile.foto_perfil.url)
                return profile.foto_perfil.url
        except:
            pass
        return None
