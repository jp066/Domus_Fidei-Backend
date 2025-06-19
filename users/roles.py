from rolepermissions.roles import AbstractUserRole # importa AbstractUserRole da biblioteca rolepermissions
# o AbstractUserRole é uma classe base que define os papéis de usuário e suas permissões

class Paroco(AbstractUserRole):
    available_permissions = {
        'manage_parish': True, # Permissão para gerenciar a paróquia
        'manage_masses': True, # Permissão para gerenciar missas
        'sacraments': True, # Permissão para gerenciar sacramentos
        'manage_ministries': True, # Permissão para gerenciar ministérios
        'manage_notifications': True, # Permissão para gerenciar notificações
        'manage_prayer_requests': True, # Permissão para gerenciar pedidos de oração
        'edit_events': True, # Permissão para editar eventos
        'manage_finances': True, # Permissão para gerenciar finanças
    }

class Pascom(AbstractUserRole):
    available_permissions = {
        'create_midia': True, # Permissão para criar mídia
        'edit_midia': True, # Permissão para editar mídia
        'delete_midia': True, # Permissão para deletar mídia
        'view_midia': True, # Permissão para visualizar mídia
        'upload_midia': True, # Permissão para fazer upload de mídia
        'manage_finances': True, # Permissão para gerenciar finanças
                 
    }