from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SimulationView, 
    SimulationHistoryView, 
    SimulationDashboardView,
    SimulationExportPDFView,
    TaxRuleViewSet,
    SuggestionMatrixViewSet
)

# Criar roteador para ViewSets de gestão
router = DefaultRouter()
router.register(r'management/tax-rules', TaxRuleViewSet, basename='tax-rules')
router.register(r'management/suggestions', SuggestionMatrixViewSet, basename='suggestions')

urlpatterns = [
    # Simulações
    path('simulate/', SimulationView.as_view(), name='simulate'),
    path('history/', SimulationHistoryView.as_view(), name='simulation-history'),
    path('dashboard/', SimulationDashboardView.as_view(), name='simulation-dashboard'),
    path('<int:pk>/export/', SimulationExportPDFView.as_view(), name='simulation-export-pdf'),
    
    # Gestão (inclui rotas do roteador)
    path('', include(router.urls)),
]
