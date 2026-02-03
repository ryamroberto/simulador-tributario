from rest_framework import viewsets
from .models import Company
from .serializers import CompanySerializer

class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações de CRUD em Empresas.
    """
    queryset = Company.objects.all().order_by('-created_at')
    serializer_class = CompanySerializer