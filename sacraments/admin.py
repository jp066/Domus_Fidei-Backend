from django.contrib import admin
from .models import SacramentoParoquial, AgendamentoSacramento, SacramentoChoices # Importe seus modelos

# Admin para SacramentoParoquial (o "tipo" de sacramento)
@admin.register(SacramentoParoquial)
class SacramentoParoquialAdmin(admin.ModelAdmin):
    list_display = ('nome_sacramento', 'paroco_responsavel')
    search_fields = ('nome_sacramento', 'paroco_responsavel__pessoa__nome') # Pesquisa pelo nome do sacramento ou nome do pároco
    list_filter = ('nome_sacramento', 'paroco_responsavel__pessoa__nome')
    ordering = ('nome_sacramento',)

# Admin para AgendamentoSacramento (o evento agendado/realizado)
@admin.register(AgendamentoSacramento)
class AgendamentoSacramentoAdmin(admin.ModelAdmin):
    list_display = ('sacramento', 'pessoa', 'data_solicitada', 'aprovado')
    search_fields = (
        'sacramento__nome_sacramento', # Busca pelo nome do tipo de sacramento
        'pessoa__nome',               # Busca pelo nome da pessoa solicitante
        'local_evento',
        'envolvidos'
    )
    list_filter = ('aprovado', 'sacramento__nome_sacramento', 'data_solicitada')
    ordering = ('-data_solicitada',)
    
    # Adicionar campo 'data_hora_realizacao' para edição manual, se você adicionou ao modelo
    fieldsets = (
        (None, {'fields': ('sacramento', 'pessoa', 'data_solicitada', 'local_evento', 'descricao_agendamento', 'envolvidos', 'aprovado')}),
        ('Detalhamento da Realização', {'fields': ('data_hora_realizacao',)}), # Se você adicionou este campo
    )
    
    # raw_id_fields é útil aqui também para 'sacramento' e 'pessoa' se houver muitos registros
    raw_id_fields = ('sacramento', 'pessoa')