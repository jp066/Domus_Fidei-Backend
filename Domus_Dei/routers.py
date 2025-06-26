from rest_framework.routers import DefaultRouter
from users.views import PessoaViewSet
from sacraments.views import SacramentoViewSet, AgendamentoViewSet
from events.views import EventosViewSet

router = DefaultRouter()
router.register(r'pessoa', PessoaViewSet, basename='pessoa')  # Registrar o app 'users' com o namespace 'users'
router.register(r'sacramentos', SacramentoViewSet, basename='sacramentos')  # Registrar o app 'users' com o namespace 'users'
router.register(r'agendamentos', AgendamentoViewSet, basename='agendamentos')  # Registrar o app 'users' com o namespace 'users'
router.register(r'eventos', EventosViewSet, basename='eventos')  # Registrar o app 'users' com o namespace 'users'