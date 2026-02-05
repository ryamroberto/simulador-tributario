from django.urls import path
from .views import SimulationView, SimulationHistoryView

urlpatterns = [
    path('simulate/', SimulationView.as_view(), name='simulate'),
    path('history/', SimulationHistoryView.as_view(), name='simulation-history'),
]