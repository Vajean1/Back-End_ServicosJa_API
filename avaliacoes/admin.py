from django.contrib import admin
from .models import Avaliacao

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_cliente', 'get_prestador', 'nota', 'data_criacao')
    search_fields = (
        'solicitacao_contato__cliente__email', 
        'solicitacao_contato__prestador__email'
    )
    autocomplete_fields = ('solicitacao_contato',)

    @admin.display(description='Cliente')
    def get_cliente(self, obj):
        return obj.solicitacao_contato.cliente

    @admin.display(description='Prestador')
    def get_prestador(self, obj):
        return obj.solicitacao_contato.prestador
