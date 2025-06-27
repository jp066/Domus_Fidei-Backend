from django.db import models
from users.models import Paroco, Pessoa

class SacramentoChoices(models.TextChoices):
    BATISMO = 'BATISMO', 'Batismo'
    CONFISSAO = 'CONFISSAO', 'Confissão'
    CRISMA = 'CRISMA', 'Crisma'
    ADORACAO_EUCARISTICA = 'ADORACAO_EUCARISTICA', 'Adoração Eucarística'
    MATRIMONIO = 'MATRIMONIO', 'Matrimônio'
    ORDENACAO = 'ORDENACAO', 'Ordenação'
    UNCAO_DOS_ENFERMOS = 'UNCAO_DOS_ENFERMOS', 'Unção dos Enfermos'
    RECONCILIACAO = 'RECONCILIACAO', 'Reconciliação'

class SacramentoParoquial(models.Model):
    paroco_responsavel = models.ForeignKey(
        Paroco,
        on_delete=models.CASCADE,
        verbose_name='Pároco Responsável'
    )
    nome_sacramento = models.CharField(
        max_length=20,
        choices=SacramentoChoices.choices,
        null=False,
        verbose_name="Nome do Sacramento",
        default=SacramentoChoices.BATISMO,
    )

    def __str__(self):
        return f'{self.nome_sacramento} - Pe. {self.paroco_responsavel.pessoa.nome}'


class AgendamentoSacramento(models.Model): 
    # uma pessoa pode agendar um sacramento, que é um evento que ocorre em uma data específica. Agora,
    # cabe ao pároco responsável aprovar ou não o agendamento.
    sacramento = models.ForeignKey(
        SacramentoParoquial,
        on_delete=models.CASCADE,
        verbose_name='Sacramento',
        related_name='agendamentos'
    ) 
    # para agendar um sacramento, é necessário que ele já exista no sistema. exemplo: so posso agendar um batismo como algo criado 
    # (sem só inserir como texto, que é como acontece em um Gerenciador de tarefas por exemplo).
    # exemplo de uso:
    # sacramento = SacramentoParoquial.objects.get(id=1) # digamos que o sacramento com id 1 é um batismo etc.

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        verbose_name='Pessoa',
        related_name='agendamentos_sacramento'
    ) # uma pessoa pode agendar vários sacramentos, mas cada agendamento é feito por uma única pessoa.
      # po exemplo: uma pessoa pode agendar um batismo, uma crisma e um matrimônio, mas cada agendamento é feito por ela.

    data_agendamento = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data do Agendamento'
    )

    data_solicitada = models.DateTimeField(
        null=False,
        verbose_name='Data Solicitada',
        help_text='Data em que o sacramento foi solicitado.'
    ) # data em que o sacramento foi solicitado, ou seja, a data que a pessoa escolheu para o sacramento.


    aprovado = models.BooleanField( 
        # só utilizado em casos de sacramentos que não necessitam do paroco para serem realizados, podendo ser
        # realizados por diáconos, catequistas ou outros ministros.
        # o pároco responsável deve aprovar o sacramento após a realização.
        default=False,
        verbose_name='Aprovado',
        help_text='Indica se o sacramento foi aprovado pelo pároco responsável.'
    )

    class Meta:
        verbose_name = 'Agendamento de Sacramento'
        verbose_name_plural = 'Agendamentos de Sacramentos'

    def __str__(self):
        return f'{self.sacramento.nome_sacramento} - {self.pessoa.nome} - {self.data_solicitada.strftime("%Y-%m-%d %H:%M:%S")}'