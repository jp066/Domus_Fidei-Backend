from django.db import models
from events.models import InscricaoRetiro

class StatusPagamento(models.TextChoices):
    PENDENTE = 'pendente', 'Pendente'
    APROVADO = 'aprovado', 'Aprovado'
    RECUSADO = 'recusado', 'Recusado'
    ESTORNADO = 'estornado', 'Estornado'
    EXPIRADO = 'expirado', 'Expirado'


class PagamentoRetiro(models.Model):
    inscricao = models.ForeignKey(
        InscricaoRetiro,
        on_delete=models.CASCADE,
        related_name='pagamentos'
    )
    data_pagamento = models.DateField(auto_now_add=True)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    comprovante_pagamento = models.FileField(
        upload_to='comprovantes_pagamento/',
        verbose_name='Comprovante de Pagamento',
        null=True,
        blank=True
    )
    data_vencimento = models.DateField(null=True, blank=True)
    codigo_barras = models.CharField(max_length=150, null=True, blank=True)
    gateway_id = models.CharField(max_length=100, null=True, blank=True)
    status_gateway = models.CharField(max_length=50, default='pendente')
    metodo_pagamento = models.CharField(max_length=50, null=True, blank=True)
    url_pagamento = models.URLField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=StatusPagamento.choices,
        default=StatusPagamento.PENDENTE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def atualizar_status(self, status_gateway_recebido):
        self.status_gateway = status_gateway_recebido
        mapeamento = {
            'paid': StatusPagamento.APROVADO,
            'pending': StatusPagamento.PENDENTE,
            'refused': StatusPagamento.RECUSADO,
            'refunded': StatusPagamento.ESTORNADO,
            'expired': StatusPagamento.EXPIRADO,
        }
        self.status = mapeamento.get(status_gateway_recebido, StatusPagamento.PENDENTE)
        self.save()

    def __str__(self):
        return f"Pagamento de R${self.valor_pago} para a inscrição {self.inscricao.id} - Status: {self.status}"


class StatusTentativaPagamento(models.TextChoices):
    CRIADA = 'criada', 'Criada'
    ENVIADA = 'enviada', 'Enviada ao gateway'
    SUCESSO = 'sucesso', 'Sucesso'
    FALHA = 'falha', 'Falha'
    ERRO = 'erro', 'Erro'


class TentativaPagamento(models.Model):
    pagamento = models.ForeignKey(PagamentoRetiro, on_delete=models.CASCADE, related_name='tentativas')
    status = models.CharField(max_length=20, choices=StatusTentativaPagamento.choices)
    data_tentativa = models.DateTimeField(auto_now_add=True)
    resposta_gateway = models.JSONField(null=True, blank=True)