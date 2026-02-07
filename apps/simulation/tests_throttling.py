from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from simulation.models import SimulationLog
from decimal import Decimal
from django.core.cache import cache

class ThrottlingTestCase(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username="throttleuser", password="password123")
        self.client.force_authenticate(user=self.user)
        # Criar um log para poder exportar PDF
        self.log = SimulationLog.objects.create(
            user=self.user,
            monthly_revenue=Decimal('10000.00'),
            costs=Decimal('2000.00'),
            tax_regime='SIMPLES_NACIONAL',
            sector='SERVICOS',
            current_tax_load=Decimal('1000.00'),
            reform_tax_load=Decimal('2000.00'),
            delta_value=Decimal('1000.00'),
            impact_classification='NEGATIVO'
        )

    def test_export_throttling_limit(self):
        """Testa se o limite de exportação (10/min) é respeitado"""
        url = reverse('simulation-history-export')
        
        # Fazer 10 requisições - Devem passar
        for i in range(10):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK, f"Falha na requisição {i+1}")
        
        # 11ª requisição - Deve falhar (429)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS, "Deveria ter retornado 429 na 11ª requisição")
        
        # Validar mensagem em PT-BR
        self.assertIn("Limite de requisições excedido", response.data['detail'])
        self.assertIn("Tente novamente em", response.data['detail'])

    def test_global_user_throttling(self):
        """Testa o throttle global de usuário (1000/day -> não vamos fazer 1000 requisições aqui)
        Para testar o global, vamos apenas validar que as views principais têm as classes de throttle.
        Como o teste de 1000 requisições é inviável em unit test, validamos a configuração.
        """
        from simulation.views import SimulationView
        view = SimulationView()
        throttles = view.get_throttles()
        # SimulationView não tem throttle_classes explícito, então usa o DEFAULT do settings
        # que configuramos como [AnonRateThrottle, UserRateThrottle]
        self.assertTrue(len(throttles) >= 1)