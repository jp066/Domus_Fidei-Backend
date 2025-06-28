from django.db import models
from Domus_Dei import settings
from users.models import Paroco
from django.contrib.auth import get_user_model

# a classe Eventos representa um evento de algum grupo ou movimento da paróquia, como encontros, terços, etc.
# é algo mais basico do que um retiro ou acampamento, e pode ser criado por qualquer usuário com permissão de criar eventos.
# sem a necessidade de ter uma equipe.

class Eventos(models.Model):
    nome_evento = models.CharField(max_length=100, null=False, blank=False)
    descricao = models.TextField()
    data_inicio = models.DateField(null=False, blank=False)
    data_fim = models.DateField(null=False, blank=False)
    local = models.CharField(max_length=100, null=False, blank=False)
    ativo = models.BooleanField(default=True) # o evento pode ser desativado, mas não excluído
    coordenador = models.ForeignKey(
        get_user_model(), # é a mesma coisa que Pessoa, mas aqui usamos get_user_model() para garantir que estamos usando o modelo de usuário correto
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    


class AssembleiaParoquial(models.Model):
    tema_assembleia = models.CharField(max_length=100)
    data_assembleia = models.DateField()
    local = models.CharField(max_length=100)
    participantes = models.ManyToManyField(
        get_user_model(),
        related_name='assembleias_participantes',
        blank=True,
        help_text='Usuários convidados para a assembleia'
    ) # para isso, é necessario criar um modelo?
    # o 
    ativo = models.BooleanField(default=True) # a assembleia pode ser desativada, mas não excluída
    paroco = models.ForeignKey(
        Paroco,
        on_delete=models.CASCADE,
        related_name='assembleias_paroquiais'
    )


# o responsável é o usuário que criou a formação, pode ser um pároco ou outro membro da comunidade
# diferente da AssembleiaParoquial, a formação não precisa ser necessariamente conduzida por um pároco,
# mas pode ser conduzida por outros membros da comunidade ou convidados.
# no entanto, só pode ser criada por um usuário com permissão de criar formações.
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='retiros_coordenados'
    ) # o coordenador é o usuário que criou o retiro/acampamento
    logo = models.FileField(
        upload_to='midias_galeria/',
        verbose_name='Arquivo da Mídia'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EquipeRetiro(models.Model):
    retiro = models.ForeignKey(RetiroAcampamento, on_delete=models.CASCADE, related_name='equipes')
    nome_equipe = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome_equipe} - {self.retiro.nome_retiro}"
    class Meta:
        verbose_name = 'Equipe de Evento'
        verbose_name_plural = 'Equipes de Eventos'
        ordering = ['nome_equipe']


class ServoRetiro(models.Model):
    retiro = models.ForeignKey(RetiroAcampamento, on_delete=models.CASCADE, related_name='membros_equipe')
    equipe = models.ForeignKey(EquipeRetiro, on_delete=models.CASCADE, related_name='membros')
    servo = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='servos_retiro'
    )  # o servo é o usuário que faz parte da equipe do retiro/acampamento


class CronogramaRetiro(models.Model):
    retiro = models.ForeignKey(RetiroAcampamento, on_delete=models.CASCADE, related_name='cronogramas')
    titulo = models.CharField(max_length=100) # 
    descricao = models.TextField()
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField()
    local = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.retiro.nome_retiro}"


class StatusInscricaoRetiro(models.TextChoices):
    PENDENTE = 'P', 'Pendente'
    CONFIRMADA = 'C', 'Confirmada'
    CANCELADA = 'X', 'Cancelada'


class InscricaoRetiro(models.Model):
    retiro = models.ForeignKey(RetiroAcampamento, on_delete=models.CASCADE, related_name='inscricoes')
    usuario = models.CharField(max_length=100)  # Nome do inscrito
    email = models.EmailField(null=True, blank=True)  # Opcional, caso queira contato
    telefone = models.CharField(max_length=20, null=True, blank=True)  # Opcional
    data_inscricao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1,
        choices=StatusInscricaoRetiro.choices,
        default=StatusInscricaoRetiro.PENDENTE
    )
    observacoes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Inscrição de {self.usuario} no retiro {self.retiro.nome_retiro} - Status: {self.get_status_display()}"