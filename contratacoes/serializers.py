from rest_framework import serializers
from .models import SolicitacaoContato
from django.contrib.auth import get_user_model

User = get_user_model()

class ContatoSerializer(serializers.ModelSerializer):
    # Recebemos apenas os IDs
    prestador_id = serializers.PrimaryKeyRelatedField(
        source='prestador', 
        queryset=User.objects.filter(tipo_usuario='prestador')
    )
    
    class Meta:
        model = SolicitacaoContato
        fields = ['prestador_id', 'servico']

    def validate(self, data):
        # Evita que prestador contate a si mesmo
        request = self.context.get('request')
        if request and request.user == data['prestador']:
            raise serializers.ValidationError("Você não pode iniciar contato consigo mesmo.")
        return data
