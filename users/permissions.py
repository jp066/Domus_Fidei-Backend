from rest_framework.permissions import BasePermission

class PerfilPermitido(BasePermission):
    def __init__(self, *perfis):
        self.perfis = perfis

    def has_permission(self, request, view):
        if request.user.is_authenticated: # verifica se o usuário está autenticado
            return request.user.perfil in self.perfis
        return False