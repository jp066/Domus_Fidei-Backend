from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class PerfilPermitido(BasePermission):
    def __init__(self, *perfis):
        self.perfis = perfis

    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado
        if not request.user or not request.user.is_authenticated:
            return False
            
        perfil_pessoa = getattr(request.user, 'perfil_pessoa', None)
        perfis_adicionais = getattr(request.user, 'perfis_adicionais', None)
        
        # Verifica se o perfil principal está nos perfis permitidos
        if perfil_pessoa in self.perfis:
            return True
            
        # Verifica se algum dos perfis adicionais está nos perfis permitidos
        if perfis_adicionais:
            if perfis_adicionais in self.perfis:
                return True
        
        return False