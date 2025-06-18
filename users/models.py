from django.db import models

class PerfilUsuario(models.TextChoices):
    PAROCO = 'PAROCO', 'Pároco'
    CATEQUISTA = 'CATEQUISTA', 'Catequista'
    COORDENADOR_MINISTERIO = 'COORD_MINISTERIO', 'Coordenador de Ministério'
    PASCOM = 'PASCOM', 'PASCOM'
    FIEL = 'FIEL', 'Fiel da Comunidade'


class Usuario(models.Model):
    codigo_acesso = models.CharField(
        max_length=100,
        primary_key=True,
        verbose_name='Código de Acesso'
    )
    comunidade = models.CharField(max_length=100, verbose_name='Comunidade')
    perfil_usuario = models.CharField(
        max_length=20,
        choices=PerfilUsuario.choices,
        default=PerfilUsuario.FIEL,
        verbose_name="Perfil do Usuário"
    )

    identificador_paroco = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Identificador do Pároco'
    )