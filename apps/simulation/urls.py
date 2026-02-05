from django.urls import path
from .views import (
    SimulationView, 
    SimulationHistoryView, 
    SimulationDashboardView,
    SimulationExportPDFView
)

urlpatterns = [
    path('simulate/', SimulationView.as_view(), name='simulate'),
    path('history/', SimulationHistoryView.as_view(), name='simulation-history'),
    path('dashboard/', SimulationDashboardView.as_view(), name='simulation-dashboard'),
    path('<int:pk>/export/', SimulationExportPDFView.as_view(), name='simulation-export-pdf'),
]