from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # Importa o UserAdmin padrão do Django
from .models import Pessoa, Paroco, PerfilPessoa # Importa seus modelos
# Importa o PerfilPessoa para usar como choices no campo perfil_pessoa

class PessoaAdmin(BaseUserAdmin): # Herda do UserAdmin padrão do Django
    # Campos que serão exibidos na lista de objetos no painel de admin
    list_display = ('codigo_acesso', 'nome', 'perfil_pessoa', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('codigo_acesso', 'nome', 'comunidade', 'perfil_pessoa')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'perfil_pessoa')
    ordering = ('perfil_pessoa', 'nome')
    fieldsets = (
        (None, {'fields': ('password',)}), # Informações de autenticação
        ('Informações Pessoais', {'fields': ('nome', 'comunidade', 'perfil_pessoa')}),
        ('Permissões e Status', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    ) # fieldsets são usados para organizar os campos no formulário de edição do usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nome', 'comunidade', 'perfil_pessoa', 'password'), # Inclua password aqui
        }),
    )
    
    # Permite o gerenciamento de ManyToManyField (groups e user_permissions) com um widget mais amigável
    filter_horizontal = ('groups', 'user_permissions',)

    # Método save_model para atribuir roles com django-role-permissions
    # Este método é chamado quando um objeto é salvo via admin.
    def save_model(self, request, obj, form, change):
        from rolepermissions.roles import assign_role, remove_role, get_user_roles
        from .roles import Paroco, Catequista, CoordenadorMinisterio, Pascom, Fiel

        # Senhas temporárias ou lógica de primeiro login, se for o caso
        # Se você quer que o usuário defina a própria senha, NÃO preencha 'password' aqui.
        # Apenas use obj.set_password(form.cleaned_data["password"]) se for um novo usuário ou a senha mudou.
        # No seu caso, o usuário definirá a senha no primeiro acesso.
        # O AbstractUser já cuida do hashing da senha quando o campo 'password' é preenchido.
        if 'password' in form.cleaned_data and form.cleaned_data['password']:
            obj.set_password(form.cleaned_data['password'])
        else:
             if obj.pk: # Se for uma edição de um usuário existente
                 original_obj = self.model.objects.get(pk=obj.pk)
                 obj.password = original_obj.password

        super().save_model(request, obj, form, change) # Salva o objeto primeiro

        # Mapeamento de PerfilPessoa para Roles (use o mesmo que você planeja para os signals)
        ROLE_MAPPING = {
            PerfilPessoa.PAROCO: Paroco,
            PerfilPessoa.CATEQUISTA: Catequista,
            PerfilPessoa.COORDENADOR_MINISTERIO: CoordenadorMinisterio,
            PerfilPessoa.PASCOM: Pascom,
            PerfilPessoa.FIEL: Fiel,
        }

        # Remove todos os papéis existentes do usuário antes de atribuir o novo
        # Isso garante que um usuário só tenha um papel principal de PerfilPessoa
        current_roles = get_user_roles(obj)
        for role_instance in current_roles:
            remove_role(obj, type(role_instance))

        # Atribui o novo papel com base no perfil_pessoa
        desired_role_class = ROLE_MAPPING.get(obj.perfil_pessoa)
        if desired_role_class:
            assign_role(obj, desired_role_class)

# Registra o modelo Pessoa com o admin personalizado
admin.site.register(Pessoa, PessoaAdmin)

# Admin para o modelo Paroco
@admin.register(Paroco) # Decorator mais conciso para registrar
class ParocoAdmin(admin.ModelAdmin):
    list_display = ('pessoa_nome', 'identificador_paroco')
    search_fields = ('pessoa__nome', 'identificador_paroco') # Pesquisa pelo nome da pessoa relacionada
    ordering = ('pessoa__nome',)
    # Se você quiser que o campo 'pessoa' seja um campo de texto de busca em vez de um dropdown gigante
    raw_id_fields = ('pessoa',) # Útil para ForeignKeys com muitos objetos

    def pessoa_nome(self, obj):
        return obj.pessoa.nome
    pessoa_nome.short_description = 'Nome da Pessoa'