from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib.parse import quote
from .models import SolicitacaoContato
from .serializers import ContatoSerializer

class IniciarContatoWhatsAppView(APIView):
    """
    Recebe o interesse do cliente, registra no banco e retorna
    o link direto para o WhatsApp do prestador.
    """
    permission_classes = [permissions.IsAuthenticated] # Só clientes logados podem clicar

    def post(self, request):
        serializer = ContatoSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            prestador_user = serializer.validated_data['prestador']
            servico = serializer.validated_data['servico']
            cliente_user = request.user

            # Salva o Log no banco de dados
            SolicitacaoContato.objects.create(
                cliente=cliente_user,
                prestador=prestador_user,
                servico=servico
            )

            # Pegamos o telefone do perfil do prestador
            telefone = prestador_user.perfil_prestador.telefone_publico
            
            if not telefone:
                return Response(
                    {"erro": "Este prestador não possui telefone cadastrado."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Garante formato internacional (Brasil +55)
            telefone_formatado = f"55{telefone}" 

            # Monta a mensagem personalizada
            mensagem = (
                f"Olá {prestador_user.first_name}! "
                f"Me chamo {cliente_user.first_name}. "
                f"Encontrei seu perfil no *ServiçoJá* e gostaria de um orçamento para *{servico.nome}*."
            )
            
            # Codifica a mensagem para URL (transforma espaços em %20, etc)
            mensagem_encoded = quote(mensagem)

            # 4. Gera o Link Final
            whatsapp_url = f"https://api.whatsapp.com/send?phone={telefone_formatado}&text={mensagem_encoded}"

            # 5. Retorna para o Front-end
            return Response({
                "sucesso": True,
                "whatsapp_url": whatsapp_url
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
