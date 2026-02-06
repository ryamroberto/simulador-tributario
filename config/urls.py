from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.views import UserRegistrationView

# Decorar views de terceiros para o Swagger
DecoratedTokenObtainPairView = extend_schema_view(
    post=extend_schema(
        summary="Realizar Login (Obter Token)",
        description="Recebe as credenciais de usuário e retorna um par de tokens (Access e Refresh).",
        tags=['Autenticação']
    )
)(TokenObtainPairView)

DecoratedTokenRefreshView = extend_schema_view(
    post=extend_schema(
        summary="Renovar Token de Acesso",
        description="Recebe um token de Refresh válido e retorna um novo token de Access.",
        tags=['Autenticação']
    )
)(TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticação
    path('api/token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/register/', UserRegistrationView.as_view(), name='user_register'),

    # Apps
    path('api/companies/', include('companies.urls')),
    path('api/simulation/', include('simulation.urls')),

    # Documentação
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
