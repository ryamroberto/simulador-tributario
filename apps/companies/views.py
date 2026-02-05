from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Company
from .serializers import CompanySerializer

@extend_schema_view(
    list=extend_schema(summary="Listar Empresas", tags=['Empresas']),
    create=extend_schema(summary="Cadastrar Empresa", tags=['Empresas']),
    retrieve=extend_schema(summary="Obter Detalhes da Empresa", tags=['Empresas']),
    update=extend_schema(summary="Atualizar Empresa", tags=['Empresas']),
    partial_update=extend_schema(summary="Atualizar Empresa (Parcial)", tags=['Empresas']),
    destroy=extend_schema(summary="Remover Empresa", tags=['Empresas']),
)
class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações de CRUD em Empresas.
    """
    queryset = Company.objects.all().order_by('-created_at')
    serializer_class = CompanySerializer
