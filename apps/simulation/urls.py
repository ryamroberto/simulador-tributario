from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SimulationView,
    SimulationHistoryView,
    SimulationDashboardView,
    SimulationExportPDFView,
    SimulationHistoryExportView,
    TaxRuleViewSet,
    SuggestionMatrixViewSet
)

# Criar roteador para ViewSets de gestão
router = DefaultRouter()
router.register(r'management/tax-rules', TaxRuleViewSet, basename='tax-rules')
router.register(r'management/suggestions', SuggestionMatrixViewSet, basename='suggestions')

urlpatterns = [
    # Rota de Debug (pode remover depois)
    path('debug-excel-export/', SimulationHistoryExportView.as_view(), name='debug-excel-export'),

    # Exportação de Histórico (Nome único para evitar conflito)
    path('export-all-history/', SimulationHistoryExportView.as_view(), name='simulation-history-export'),

    # Exportação em Excel (URL específica)
    path('export-all-history/excel/', SimulationHistoryExportView.as_view(), name='simulation-history-export-excel'),
    
    # Simulações
    path('simulate/', SimulationView.as_view(), name='simulate'),
    path('history/', SimulationHistoryView.as_view(), name='simulation-history'),
    path('dashboard/', SimulationDashboardView.as_view(), name='simulation-dashboard'),
    
    # Exportação Individual
    path('export-pdf/<int:pk>/', SimulationExportPDFView.as_view(), name='simulation-export-pdf'),
    
    # Gestão
    path('', include(router.urls)),
]
