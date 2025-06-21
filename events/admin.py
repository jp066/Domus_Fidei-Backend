from django.contrib import admin
from .models import (
    Eventos, AssembleiaParoquial, Formacoes, RetiroAcampamento,
    EquipeRetiro, ServoRetiro, CronogramaRetiro, InscricaoRetiro)
from django.contrib.auth import get_user_model # Importar aqui para evitar problemas de importação

# Admin para Eventos
@admin.register(Eventos)
class EventosAdmin(admin.ModelAdmin):
    list_display = ('nome_evento', 'local', 'data_inicio', 'data_fim', 'coordenador', 'ativo')
    search_fields = ('nome_evento', 'descricao', 'local', 'coordenador__nome')
    list_filter = ('ativo', 'data_inicio', 'data_fim')
    ordering = ('-data_inicio',)
    raw_id_fields = ('coordenador',)


# Admin para AssembleiaParoquial
@admin.register(AssembleiaParoquial)
class AssembleiaParoquialAdmin(admin.ModelAdmin):
    list_display = ('tema_assembleia', 'data_assembleia', 'local', 'paroco', 'ativo')
    search_fields = ('tema_assembleia', 'local', 'paroco__pessoa__nome')
    list_filter = ('ativo', 'data_assembleia', 'paroco')
    ordering = ('-data_assembleia',)
    filter_horizontal = ('participantes',) # Para ManyToManyField
    raw_id_fields = ('paroco',)

# Admin para Formacoes
@admin.register(Formacoes)
class FormacoesAdmin(admin.ModelAdmin):
    list_display = ('tema_formacao', 'data_formacao', 'local', 'responsavel', 'ativo')
    search_fields = ('tema_formacao', 'local', 'responsavel__nome')
    list_filter = ('ativo', 'data_formacao', 'responsavel')
    ordering = ('-data_formacao',)
    filter_horizontal = ('participantes',)
    raw_id_fields = ('responsavel',)

# Inline para EquipeRetiro e CronogramaRetiro dentro de RetiroAcampamento
# Inlines permitem editar modelos relacionados diretamente na página do modelo pai
class EquipeRetiroInline(admin.TabularInline):
    model = EquipeRetiro
    extra = 1
    fields = ('nome_equipe',)


class CronogramaRetiroInline(admin.TabularInline):
    model = CronogramaRetiro
    extra = 1
    fields = ('titulo', 'descricao', 'data_hora_inicio', 'data_hora_fim', 'local')

# Inline para InscricaoRetiro dentro de RetiroAcampamento
class InscricaoRetiroInline(admin.TabularInline):
    model = InscricaoRetiro
    extra = 0 # Não mostrar formulários vazios, apenas os existentes
    fields = ('usuario', 'data_inscricao', 'status', 'observacoes')
    readonly_fields = ('data_inscricao',)

# Admin para RetiroAcampamento
@admin.register(RetiroAcampamento)
class RetiroAcampamentoAdmin(admin.ModelAdmin):
    list_display = ('nome_retiro', 'local', 'data_inicio', 'data_fim', 'coordenador', 'limite_participantes', 'ativo')
    search_fields = ('nome_retiro', 'descricao', 'local', 'coordenador__nome')
    list_filter = ('ativo', 'data_inicio', 'data_fim')
    ordering = ('-data_inicio',)
    inlines = [EquipeRetiroInline, CronogramaRetiroInline, InscricaoRetiroInline] # Adiciona os inlines
    raw_id_fields = ('coordenador',)

    def nome_retiro(self, obj):
        return obj.retiro.nome_retiro
    nome_retiro.short_description = 'Nome do Retiro'    
    # Campo calculado para participantes confirmados (se você removeu numero_participantes do modelo)
    # def get_numero_participantes_confirmados(self, obj):
    #     return obj.inscricoes.filter(status=StatusInscricaoRetiro.CONFIRMADA).count()
    # get_numero_participantes_confirmados.short_description = 'Participantes Confirmados'
    # list_display += ('get_numero_participantes_confirmados',) # Adicione à list_display se usar

# Admin para EquipeRetiro
@admin.register(EquipeRetiro)
class EquipeRetiroAdmin(admin.ModelAdmin):
    list_display = ('nome_equipe', 'nome_retiro')
    search_fields = ('nome_equipe', 'retiro__nome_retiro')
    list_filter = ('retiro',)
    ordering = ('nome_equipe',)
    raw_id_fields = ('retiro',)

    def nome_retiro(self, obj):
        return obj.retiro.nome_retiro
    nome_retiro.short_description = 'Nome do Retiro'

# Admin para ServoRetiro
@admin.register(ServoRetiro)
class ServoRetiroAdmin(admin.ModelAdmin):
    list_display = ('nome_servo', 'equipe', 'nome_retiro')
    search_fields = ('servo__nome', 'equipe__nome_equipe', 'retiro__nome_retiro')
    list_filter = ('equipe', 'retiro')
    raw_id_fields = ('retiro', 'equipe', 'servo')
    def nome_retiro(self, obj):
        return obj.retiro.nome_retiro
    nome_retiro.short_description = 'Nome do Retiro'

    def nome_servo(self, obj):
        return obj.servo.nome
    nome_servo.short_description = 'Nome do Servo'

# Admin para CronogramaRetiro
@admin.register(CronogramaRetiro)
class CronogramaRetiroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'nome_retiro', 'data_hora_inicio', 'data_hora_fim')
    search_fields = ('titulo', 'descricao', 'retiro__nome_retiro')
    list_filter = ('retiro', 'data_hora_inicio')
    ordering = ('data_hora_inicio',)
    raw_id_fields = ('retiro',)
    def nome_retiro(self, obj):
        return obj.retiro.nome_retiro
    nome_retiro.short_description = 'Nome do Retiro'

# Admin para InscricaoRetiro
@admin.register(InscricaoRetiro)
class InscricaoRetiroAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nome_retiro', 'data_inscricao')
    search_fields = ('usuario__nome', 'retiro__nome_retiro', 'observacoes')
    list_filter = ('status', 'retiro', 'data_inscricao')
    ordering = ('-data_inscricao',)
    raw_id_fields = ('retiro',)
    def nome_retiro(self, obj):
        return obj.retiro.nome_retiro
    nome_retiro.short_description = 'Nome do Retiro'