from django.contrib import admin
from .models import SolicitacaoContato

@admin.register(SolicitacaoContato)
class SolicitacaoContatoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'prestador', 'servico', 'data_clique')
    list_filter = ('data_clique',)
    search_fields = ('cliente__email', 'prestador__email')
