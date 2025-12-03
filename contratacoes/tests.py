from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import SolicitacaoContato
from servicos.models import Servico, CategoriaServico
from accounts.models import PrestadorProfile, ClienteProfile
from unittest.mock import patch

User = get_user_model()

class SolicitacaoPrestadorTests(APITestCase):
    
    @patch('accounts.models.requests.get')
    def setUp(self, mock_get):
        # Mock external API calls for address to prevent network errors and speed up tests
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'city': 'Fortaleza', 
            'neighborhood': 'Centro', 
            'state': 'CE',
            'location': {'coordinates': {'latitude': -3.7, 'longitude': -38.5}},
            'localidade': 'Fortaleza', # For ViaCEP fallback structure
            'uf': 'CE',
            'bairro': 'Centro',
            'logradouro': 'Rua Teste'
        }

        # Create Prestador User
        self.prestador = User.objects.create_user(
            email='prestador@test.com',
            username='prestador',
            nome_completo='Prestador Teste',
            password='password123',
            tipo_usuario='prestador'
        )
        # Manually create profile if not created by signal
        if not hasattr(self.prestador, 'perfil_prestador'):
            PrestadorProfile.objects.create(
                user=self.prestador,
                cep='60000000',
                rua='Rua Teste',
                numero_casa='123',
                telefone_publico='85999999999'
            )

        # Create Cliente User
        self.cliente = User.objects.create_user(
            email='cliente@test.com',
            username='cliente',
            nome_completo='Cliente Teste',
            password='password123',
            tipo_usuario='cliente'
        )
        if not hasattr(self.cliente, 'perfil_cliente'):
            ClienteProfile.objects.create(
                user=self.cliente,
                cep='60000000',
                rua='Rua Cliente',
                numero_casa='456',
                telefone_contato='85988888888'
            )
        
        # Create Service Category and Service
        self.categoria = CategoriaServico.objects.create(nome='Limpeza')
        self.servico = Servico.objects.create(
            nome='Faxina', 
            categoria=self.categoria
        )
        
        # Create solicitation
        self.solicitacao = SolicitacaoContato.objects.create(
            cliente=self.cliente,
            prestador=self.prestador,
            servico=self.servico
        )
        
        self.url = reverse('prestador-solicitacoes')

    def test_list_solicitacoes_authenticated(self):
        """
        Ensure authenticated prestador can see their solicitations.
        """
        self.client.force_authenticate(user=self.prestador)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.solicitacao.id)
        # Check if fields match serializer output
        self.assertEqual(response.data[0]['cliente_nome'], self.cliente.nome_completo)
        self.assertEqual(response.data[0]['servico_nome'], self.servico.nome)

    def test_list_solicitacoes_unauthenticated(self):
        """
        Ensure unauthenticated user cannot see solicitations.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('accounts.models.requests.get')
    def test_list_solicitacoes_wrong_user(self, mock_get):
        """
        Ensure a different user (e.g. another prestador) does not see this solicitation.
        """
        # Mock for the new user profile creation
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {}

        other_prestador = User.objects.create_user(
            email='other@test.com',
            username='other',
            nome_completo='Other',
            password='password123',
            tipo_usuario='prestador'
        )
        self.client.force_authenticate(user=other_prestador)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
