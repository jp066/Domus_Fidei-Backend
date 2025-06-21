from django.db import models
from Domus_Dei import settings
from users.models import Paroco
from django.contrib.auth import get_user_model

# a classe Eventos representa um evento de algum grupo ou movimento da paróquia, como encontros, terços, etc.
class Eventos(models.Model):
    nome_evento = models.CharField(max_length=100)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    local = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True) # o evento pode ser desativado, mas não excluído
    coordenador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='eventos_coordenados'
    ) # o coordenador é o usuário que criou o evento
    logo = models.FileField(
        upload_to='midias_galeria/', 
        verbose_name='Arquivo da Mídia',
        null=True,
        blank=True,
        # o logo do evento é opcional, mas se existir, deve ser carregado aqui, porque um retiro deve ter uma logo
        # mas um evento normal não precisa ter uma logo.
        )
    

class AssembleiaParoquial(models.Model):
    tema_assembleia = models.CharField(max_length=100)
    data_assembleia = models.DateField()
    local = models.CharField(max_length=100)
    participantes = models.ManyToManyField(
        get_user_model(),
        related_name='assembleias_participantes',
        blank=True,
        help_text='Usuários convidados para a assembleia'
    )
    ativo = models.BooleanField(default=True) # a assembleia pode ser desativada, mas não excluída
    paroco = models.ForeignKey(
        Paroco,
        on_delete=models.CASCADE,
        related_name='assembleias_paroquiais'
    ) # o pároco é o responsável pela assembleia paroquial


class Formacoes(models.Model):
    tema_formacao = models.CharField(max_length=100)
    data_formacao = models.DateField()
    local = models.CharField(max_length=100)
    participantes = models.ManyToManyField(
        get_user_model(),
        related_name='formacoes_participadas',
        blank=True,
        help_text='Usuários convidados para a formação'
    )
    ativo = models.BooleanField(default=True) # a assembleia pode ser desativada, mas não excluída
    responsavel = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='formacoes_responsaveis',
        null=True,
        blank=True
    )
    # o responsável é o usuário que criou a formação, pode ser um pároco ou outro membro da comunidade
    # diferente da AssembleiaParoquial, a formação não precisa ser necessariamente conduzida por um pároco,
    # mas pode ser conduzida por outros membros da comunidade ou convidados.
    # no entanto, só pode ser criada por um usuário com permissão de criar formações.


class RetiroAcampamento(models.Model):
    nome_retiro = models.CharField(max_length=100)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    local = models.CharField(max_length=100)
    numero_participantes = models.IntegerField(default=0) # o numero de participantes é definido no momento da criação do retiro/acampamento
    # mas inicialmente é 0. e deve ser menor ou igual ao limite de participantes
    limite_participantes = models.IntegerField(default=0) # o limite de participantes é definido no momento da criação do retiro/acampamento
    # mas inicialmente é 0.
    custo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # o custo é definido no momento da criação do retiro/acampamento
    ativo = models.BooleanField(default=True) # o retiro/acampamento pode ser desativado, mas não excluído
    coordenador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='retiros_coordenados'
    ) # o coordenador é o usuário que criou o retiro/acampamento
    logo = models.FileField(
        upload_to='midias_galeria/',
        verbose_name='Arquivo da Mídia'
        )