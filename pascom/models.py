from django.db import models
from users.models import Pessoa

class AlbumGaleria(models.Model):
    nome_album = models.CharField(max_length=100, verbose_name='Nome do Álbum')
    descricao = models.TextField(verbose_name='Descrição do Álbum', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    id_pessoa_pascom = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, related_name='albuns_pascom')

    class Meta:
        verbose_name = 'Álbum de Galeria'
        verbose_name_plural = 'Álbuns de Galeria'
        ordering = ['-data_criacao']

    def count_midias(self):
        return self.midias.count()

    def __str__(self):
        return f'{self.nome_album} - {self.id_pessoa_pascom.nome} - {self.count_midias()} mídias'
    

class MidiaChoices(models.TextChoices):
    FOTO = 'FOTO', 'Foto'
    VIDEO = 'VIDEO', 'Vídeo'
    AUDIO = 'AUDIO', 'Áudio'


class MidiaGaleria(models.Model):
    album = models.ForeignKey(AlbumGaleria, on_delete=models.CASCADE, related_name='midias')
    tipo_midia = models.CharField(
        max_length=10,
        choices=MidiaChoices.choices,
        default=MidiaChoices.FOTO,
        verbose_name='Tipo de Mídia'
    )
    nome_arquivo = models.CharField(max_length=255, blank=True, verbose_name='Nome do Arquivo')  # <-- Adicionado
    arquivo = models.FileField(upload_to='midias_galeria/', verbose_name='Arquivo da Mídia')
    # a variavel arquivo deve ser um arquivo de imagem, vídeo ou áudio. funciona como um campo de upload de arquivos.
    data_upload = models.DateTimeField(auto_now_add=True, verbose_name='Data de Upload')
    id_pessoa_pascom = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, related_name='midias_pascom')

    class Meta:
        verbose_name = 'Mídia de Galeria'
        verbose_name_plural = 'Mídias de Galeria'
        ordering = ['-data_upload']


    # Preenche o nome_arquivo automaticamente com o nome do arquivo enviado
    def save(self, *args, **kwargs):
        if not self.nome_arquivo and self.arquivo:
            self.nome_arquivo = self.arquivo.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_arquivo} ({self.tipo_midia})"