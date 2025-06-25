from rest_framework.permissions import BasePermission

class PerfilPermitido(BasePermission):
    def __init__(self, *perfis):
        self.perfis = perfis

    def has_permission(self, request, view):
        if request.user.is_authenticated: # verifica se o usuário está autenticado
            return request.user.perfil_pessoa in self.perfis
        return False
    
    # para usar: @action(detail=False, methods=['get'], permission_classes=[PerfilPermitido('admin', 'gerente')])
#    def get_permissions(self):
#        if self.action == 'criar_material':
#            return [PerfilPermitido('CATEQUISTA')]
#        elif self.action == 'enviar_convite':
#            return [PerfilPermitido('PAROCO', 'CATEQUISTA')]
#        elif self.action == 'marcar_atendido':
#            return [PerfilPermitido('PAROCO')]
#        return []