from django.http import HttpResponse
from django.contrib.auth.models import User
from rolepermissions.permissions import revoke_permission, grant_permission
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator, has_permission_decorator 
# has_role_decorator ´é um decorador que verifica se o usuário tem um papel específico
# has_permission_decorator é um decorador que verifica se o usuário tem uma permissão específica

# has_role_decorator('paroco')  # Decorador para verificar se o usuário tem o papel de Pároco
# @has_permission_decorator('manage_finances') # Decorador para verificar se o usuário tem o papel de Pároco
# def exemplo_funcao_paroco(request):
#     grant_permission(request.user, 'manage_finances')  # Atribui a permissão de gerenciar finanças ao papel de Pároco
#     return HttpResponse("Função de exemplo para Pároco executada com sucesso!")
# 
# def criar_usuario(request):
#     user = User.objects.create_user(
#         username='joaop',
#         password='123456',)
#     user.save()
#     assign_role(user, 'paroco')  # Atribui o papel de Pároco ao usuário criado
#     return HttpResponse("Usuário criado com sucesso!")
# 
# def criar_usuario_sem_permissao(request):
#     user = User.objects.create_user(
#         username='joao',
#         password='123456',)
#     user.save()
#     assign_role(user, 'pascom')
#     return HttpResponse("Usuário criado com sucesso!")