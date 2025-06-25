from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path, include
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importar settings
from django.conf.urls.static import static # Importar static
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView  # Importar views do Simple JWT
from Domus_Dei.routers import router  # Importar o roteador definido no arquivo routers.py


schema_view = get_schema_view(
   openapi.Info(
      title="Minha API",
      default_version='v1',
      description="Documentação da API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="seu@email.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include router URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # endpoint para obter o token JWT, que fará o login.
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # endpoint para atualizar o token JWT.
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)