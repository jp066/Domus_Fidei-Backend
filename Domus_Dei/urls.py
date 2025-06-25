from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importar settings
from django.conf.urls.static import static # Importar static
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView  # Importar views do Simple JWT
from rest_framework.routers import DefaultRouter
from users.views import CriarPessoaViewSet # Importar a view CriarPessoa do app 'users'

router = DefaultRouter()
router.register(r'criar-pessoa', CriarPessoaViewSet, basename='criar-pessoa')  # Registrar o app 'users' com o namespace 'users'
router.register(r'users', CriarSacramentoViewSet, basename='users')  # Registrar o app 'users' com o namespace 'users'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # endpoint para obter o token JWT, que fará o login.
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # endpoint para atualizar o token JWT.
    path('api/', include(router.urls)),  # Include router URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)