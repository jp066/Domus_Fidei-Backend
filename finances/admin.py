from django.contrib import admin
from .models import PagamentoRetiro, TentativaPagamento, StatusPagamento, StatusTentativaPagamento

# Inline para TentativaPagamento dentro de PagamentoRetiro
class TentativaPagamentoInline(admin.TabularInline):
    model = TentativaPagamento
    extra = 0 # Mostrar apenas tentativas existentes
    fields = ('status', 'data_tentativa', 'resposta_gateway')
    readonly_fields = ('data_tentativa',)
    # Se resposta_gateway for JSONField, pode ser editável ou read-only dependendo da necessidade

# Admin para PagamentoRetiro
@admin.register(PagamentoRetiro)
class PagamentoRetiroAdmin(admin.ModelAdmin):
    list_display = ('inscricao', 'valor_pago', 'status', 'data_pagamento', 'data_vencimento')
    search_fields = ('inscricao__usuario__nome', 'inscricao__retiro__nome_retiro', 'codigo_barras', 'gateway_id')
    list_filter = ('status', 'data_pagamento', 'metodo_pagamento')
    ordering = ('-data_pagamento',)
    inlines = [TentativaPagamentoInline] # Adiciona o inline
    raw_id_fields = ('inscricao',)

# Admin para TentativaPagamento (se você quiser gerenciar separadamente também)
@admin.register(TentativaPagamento)
class TentativaPagamentoAdmin(admin.ModelAdmin):
    list_display = ('pagamento', 'status', 'data_tentativa')
    search_fields = ('pagamento__inscricao__usuario__nome', 'status')
    list_filter = ('status', 'data_tentativa')
    ordering = ('-data_tentativa',)
    raw_id_fields = ('pagamento',)