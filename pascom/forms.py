from django import forms
from .models import AlbumGaleria, MidiaGaleria

class AlbumGaleriaForm(forms.ModelForm):
    class Meta:
        model = AlbumGaleria
        fields = ['nome_album', 'descricao', 'id_pessoa_pascom'] # Inclua criado_por se for preenchido pelo usuário ou no form

    # Exemplo de como inicializar o campo criado_por com o usuário logado (na view)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['criado_por'].queryset = User.objects.all() # Se for um dropdown de usuários

class MidiaGaleriaForm(forms.ModelForm):
    class Meta:
        model = MidiaGaleria
        # 'arquivo' corresponde ao seu url_arquivo
        fields = ['album', 'tipo_midia', 'arquivo', 'id_pessoa_pascom'] # Inclua uploaded_por se for preenchido pelo usuário ou no form

    # Exemplo de como inicializar o campo uploaded_por com o usuário logado (na view)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['uploaded_por'].queryset = User.objects.all() # Se for um dropdown de usuários