from django.db import models
from django.contrib.auth.models import AbstractUser

class PerfilPessoa(models.TextChoices):
    PAROCO = 'PAROCO', 'Pároco'
    CATEQUISTA = 'CATEQUISTA', 'Catequista'
    COORDENADOR_MINISTERIO = 'COORD_MINISTERIO', 'Coordenador de Ministério'
    PASCOM = 'PASCOM', 'PASCOM'
    FIEL = 'FIEL', 'Fiel da Comunidade'


class Pessoa(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True, default=None)
    email = models.EmailField(max_length=254, null=True, blank=True, default=None)
    first_name = models.CharField(max_length=150, null=True, blank=True, default=None)
    last_name = models.CharField(max_length=150, null=True, blank=True, default=None)
    is_superuser = models.BooleanField(default=False) # Por padrão, o usuário não é um superusuário
    is_staff = models.BooleanField(default=False) # Por padrão, o usuário não é um superusuário ou membro da equipe
    is_active = models.BooleanField(default=True) # Por padrão, o usuário está ativo
    codigo_acesso = models.CharField(
        max_length=20, # (ex: "P001", "CAT0010", "FIEL_12345")
        unique=True,
        verbose_name='Código de Acesso',
        help_text='Código de acesso único para identificação do usuário na plataforma.'
    )
    nome = models.CharField(max_length=100, verbose_name='Nome completo')
    comunidade = models.CharField(max_length=100, verbose_name='Comunidade')
    perfil_pessoa = models.CharField(
        max_length=20,
        choices=PerfilPessoa.choices,
        default=PerfilPessoa.FIEL,
        verbose_name="Perfil do Usuário"
    )
    USERNAME_FIELD = 'codigo_acesso' # O campo 'codigo_acesso' será usado para login
    REQUIRED_FIELDS = ['nome', 'comunidade', 'perfil_pessoa'] # Campos obrigatórios na criação de um superusuário

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ['nome']



class Paroco(models.Model):
    pessoa = models.OneToOneField(
        Pessoa,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Pessoa'
    )
    identificador_paroco = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Identificador do Pároco'
    )