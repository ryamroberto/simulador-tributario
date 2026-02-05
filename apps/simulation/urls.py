from django.urls import path
from .views import SimulationView, SimulationHistoryView, SimulationDashboardView

urlpatterns = [
    path('simulate/', SimulationView.as_view(), name='simulate'),
    path('history/', SimulationHistoryView.as_view(), name='simulation-history'),
    path('dashboard/', SimulationDashboardView.as_view(), name='simulation-dashboard'),
]
