from django.contrib import admin
from .models import AlbumGaleria, MidiaGaleria, MidiaChoices

# Inline para MidiaGaleria dentro de AlbumGaleria
# Isso permite adicionar/editar mídias diretamente na página do álbum
class MidiaGaleriaInline(admin.TabularInline): # Ou admin.StackedInline para um layout diferente
    model = MidiaGaleria
    extra = 1 # Quantos formulários vazios mostrar para adicionar novas mídias
    fields = ('tipo_midia', 'arquivo', 'nome_arquivo', 'data_upload', 'id_pessoa_pascom')
    readonly_fields = ('data_upload', 'nome_arquivo') # Estes campos são preenchidos automaticamente

# Admin para AlbumGaleria
@admin.register(AlbumGaleria)
class AlbumGaleriaAdmin(admin.ModelAdmin):
    list_display = ('nome_album', 'id_pessoa_pascom', 'data_criacao', 'count_midias')
    search_fields = ('nome_album', 'descricao', 'id_pessoa_pascom__nome')
    list_filter = ('data_criacao', 'id_pessoa_pascom')
    ordering = ('-data_criacao',)
    inlines = [MidiaGaleriaInline] # Adiciona o inline aqui
    raw_id_fields = ('id_pessoa_pascom',)

# Admin para MidiaGaleria (se você quiser gerenciar mídias separadamente também)
@admin.register(MidiaGaleria)
class MidiaGaleriaAdmin(admin.ModelAdmin):
    list_display = ('nome_arquivo', 'tipo_midia', 'album', 'data_upload', 'id_pessoa_pascom')
    search_fields = ('nome_arquivo', 'album__nome_album', 'id_pessoa_pascom__nome')
    list_filter = ('tipo_midia', 'data_upload', 'album')
    ordering = ('-data_upload',)
    raw_id_fields = ('album', 'id_pessoa_pascom')