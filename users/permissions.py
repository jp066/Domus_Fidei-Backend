from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class PerfilPermitido(BasePermission):
    def __init__(self, *perfis):
        self.perfis = perfis


    def has_permission(self, request, view):
        perfil_pessoa = getattr(request.user, 'perfil_pessoa', None)

        if not request.user.is_authenticated:
            raise PermissionDenied("Usuário não autenticado.")

        if perfil_pessoa not in self.perfis:
            raise PermissionDenied("Seu perfil não tem permissão para esta ação.")

        return True