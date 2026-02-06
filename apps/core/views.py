from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from .serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    """
    Endpoint para registro de novos usuários.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    @extend_schema(
        summary="Registrar Novo Usuário",
        description="Cria uma conta de usuário no sistema para acesso às funcionalidades de simulação.",
        tags=['Autenticação']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)