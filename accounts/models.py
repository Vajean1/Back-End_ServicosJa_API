import requests
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator
from datetime import date
from django.forms import ValidationError
from django.core.exceptions import ValidationError as ModelValidationError
from geopy.geocoders import Nominatim
from time import sleep
from decimal import Decimal

def _sanitize_telefone(phone):
    if not phone:
        return ""
    return ''.join(filter(str.isdigit, str(phone)))

#Função para pegar lat e lon a partir do endereço, com tentativas em duas APIs
def pegar_latitude_longitude_do_endereco(cep: str | int, rua: str, numero: str | int) -> tuple:
    #debug
    #print(f"Buscando CEP: {cep} | Rua: {rua} | Num: {numero}")
    
    cep_str = str(cep)
    cep_limpo = ''.join(filter(str.isdigit, cep_str))
    
    if len(cep_limpo) != 8:
        return None, None

    def to_decimal(val):
        if val is None: return None
        return Decimal(f"{float(val):.8f}")

    #BrasilAPI
    try:
        print("Tentando BrasilAPI...")
        response = requests.get(f'https://brasilapi.com.br/api/cep/v2/{cep_limpo}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            loc = data.get('location', {})
            coords = loc.get('coordinates', {})
            
            lat = coords.get('latitude') if isinstance(coords, dict) else None
            lon = coords.get('longitude') if isinstance(coords, dict) else None
            
            if not lat and isinstance(coords, (list, tuple)) and len(coords) >= 2:
                lon, lat = coords[0], coords[1]
            
            if lat and lon:
                #print(f"BrasilAPI deu certo: {lat}, {lon}")
                return to_decimal(lat), to_decimal(lon)
            
    except Exception as e:
        print(f"Brasil API deu ruim: {e}")

    # ViaCEP + Nominatim
    try:
        viacep = requests.get(f'https://viacep.com.br/ws/{cep_limpo}/json/', timeout=5).json()
        if "erro" in viacep:
            #print("ViaCEP não encontrou o CEP.")
            return None, None
            
        cidade = viacep.get('localidade')
        uf = viacep.get('uf')
        nome_rua = rua if rua else viacep.get('logradouro', '')
        
    except Exception:
        return None, None

    geolocator = Nominatim(user_agent="ServicoJa_App_Final/1.0", timeout=10)

    # Lista de tentativas (Exato -> Rua -> Cidade)
    queries = [
        f"{nome_rua}, {numero}, {cidade} - {uf}, Brasil",
        f"{nome_rua}, {cidade} - {uf}, Brasil",           
        f"{cidade} - {uf}, Brasil"                        
    ]

    for i, query in enumerate(queries):
        try:
            if i > 0: sleep(1)
            #print(f"Tentativa Nominatim {i+1}: {query}")
            location = geolocator.geocode(query)
            if location:
                #print(f"Deu certo: {location.latitude}, {location.longitude}")
                return to_decimal(location.latitude), to_decimal(location.longitude)
        except Exception as e:
            #print(f"Erro {i+1}: {e}")
            pass

    #print("Deu tudo ruim: Nenhuma coordenada encontrada.")
    return None, None

class User(AbstractUser):
    TIPO_USUARIO_ESCOLHA = [
        ('cliente', 'Cliente'),
        ('prestador', 'Prestador de Serviço'),
    ]
    ESCOLHA_GENERO = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('P', 'Prefiro não informar'),
    ]

    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_ESCOLHA, null=True, blank=True)
    email = models.EmailField(unique=True)
    dt_nascimento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=1, choices=ESCOLHA_GENERO, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True, help_text='CPF sem pontuação')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    @property
    def idade(self) -> int:
        if not self.dt_nascimento:
            return 'Não informado.'
        hoje = date.today()
        idade = hoje.year - self.dt_nascimento.year
        if (hoje.month, hoje.day) < (self.dt_nascimento.month, self.dt_nascimento.day):
            idade -= 1
        return idade

    def clean(self):
        if self.tipo_usuario == 'cliente' and hasattr(self, 'perfil_prestador'):
            raise ValidationError("Este usuário já é prestador.")
        if self.tipo_usuario == 'prestador' and hasattr(self, 'perfil_cliente'):
            raise ValidationError("Este usuário já é cliente.")
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


class ClienteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_cliente')
    telefone_contato = models.CharField(max_length=11, blank=True, null=True, validators=[
        RegexValidator(regex=r'^\d{10,11}$', message='Apenas dígitos, 10 ou 11 caracteres.', code='invalid_telefone')
    ])
    cep = models.CharField(max_length=9, blank=True)
    rua = models.CharField(max_length=150, blank=True)
    numero_casa = models.CharField(max_length=20, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        run_geocode = False
        if self.pk:
            try:
                antigo = ClienteProfile.objects.get(pk=self.pk)
                if (antigo.cep != self.cep or antigo.rua != self.rua or antigo.numero_casa != self.numero_casa):
                    run_geocode = True
                # Força se estiver vazio
                if not self.latitude or not self.longitude:
                    run_geocode = True
            except ClienteProfile.DoesNotExist:
                run_geocode = True
        else:
            run_geocode = True

        if run_geocode and self.cep:
            lat, lon = pegar_latitude_longitude_do_endereco(self.cep, self.rua, self.numero_casa)
            if lat and lon:
                self.latitude = lat
                self.longitude = lon
            
        if self.telefone_contato:
            self.telefone_contato = _sanitize_telefone(self.telefone_contato)

        try:
            self.full_clean()
        except ModelValidationError as e:
            raise
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.email} (Cliente)"


class PrestadorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_prestador')
    biografia = models.TextField(blank=True)
    telefone_publico = models.CharField(max_length=11, blank=True, null=True, validators=[
        RegexValidator(regex=r'^\d{10,11}$', message='Apenas dígitos, 10 ou 11 caracteres.', code='invalid_telefone')
    ])
    cep = models.CharField(max_length=8)
    rua = models.CharField(max_length=150)
    numero_casa = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    disponibilidade = models.BooleanField(default=False, help_text='Disponibilidade de horário 24 horas?')
    possui_material_proprio = models.BooleanField(default=False)
    atende_fim_de_semana = models.BooleanField(default=False)
    
    foto_perfil = models.ImageField(upload_to='perfil_prestadores/', null=True, blank=True)
    nota_media_cache = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_avaliacoes_cache = models.PositiveIntegerField(default=0)
    acessos_perfil = models.PositiveIntegerField(default=0)
    total_servicos_cache = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    servicos = models.ManyToManyField('servicos.Servico', related_name='prestadores')

    class Meta:
        indexes = [
            models.Index(fields=['cep'], name='idx_cep'),
            models.Index(fields=['latitude', 'longitude'], name='idx_geo'),
        ]
    
    def save(self, *args, **kwargs):
        run_geocode = False
        if self.pk:
            try:
                antigo = PrestadorProfile.objects.get(pk=self.pk)
                
                if (antigo.cep != self.cep or antigo.rua != self.rua or antigo.numero_casa != self.numero_casa):
                    run_geocode = True
                
                if not self.latitude or not self.longitude:
                    run_geocode = True

            except PrestadorProfile.DoesNotExist:
                run_geocode = True
        else:
            run_geocode = True

        if run_geocode and self.cep:
            lat, lon = pegar_latitude_longitude_do_endereco(self.cep, self.rua, self.numero_casa)
            if lat and lon:
                self.latitude = lat
                self.longitude = lon
            
        if self.telefone_publico:
            self.telefone_publico = _sanitize_telefone(self.telefone_publico)

        try:
            self.full_clean()
        except ModelValidationError as e:
            raise
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.email})"
