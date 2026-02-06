from django.test import TestCase
from decimal import Decimal
from django.core.cache import cache
from simulation.services.calculator import TaxCalculator
from simulation.services.analyzer import ImpactAnalyzer
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from simulation.models import SimulationLog

class OwnershipAPITest(APITestCase):
    """
    Testes de isolamento de dados entre usuários (Data Ownership).
    """
    def setUp(self):
        cache.clear()
        # Usuário A
        self.user_a = User.objects.create_user(username="usera", password="password123")
        # Usuário B
        self.user_b = User.objects.create_user(username="userb", password="password123")
        
        # Dados do Usuário A
        self.log_a = SimulationLog.objects.create(
            user=self.user_a,
            monthly_revenue=Decimal('10000.00'),
            costs=Decimal('2000.00'),
            tax_regime='SIMPLES_NACIONAL',
            sector='SERVICOS',
            current_tax_load=Decimal('1000.00'),
            reform_tax_load=Decimal('2120.00'),
            delta_value=Decimal('1120.00'),
            impact_classification='NEGATIVO'
        )

    def test_user_b_cannot_see_user_a_history(self):
        # Autenticar como B
        self.client.force_authenticate(user=self.user_b)
        url = reverse('simulation-history')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # B deve ver lista vazia, pois não tem simulações
        self.assertEqual(len(response.data['results']), 0)

    def test_user_b_cannot_export_user_a_pdf(self):
        # Autenticar como B
        self.client.force_authenticate(user=self.user_b)
        # Tentar exportar o log que pertence ao A
        url = reverse('simulation-export-pdf', kwargs={'pk': self.log_a.pk})
        response = self.client.get(url)
        
        # Deve retornar 404 porque o queryset do B é filtrado e não encontra o ID do A
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_a_sees_own_history(self):
        # Autenticar como A
        self.client.force_authenticate(user=self.user_a)
        url = reverse('simulation-history')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.log_a.id)

    def test_dashboard_aggregation_is_private(self):
        # Criar um dado para B
        SimulationLog.objects.create(
            user=self.user_b,
            monthly_revenue=Decimal('50000.00'),
            costs=Decimal('0.00'),
            tax_regime='LUCRO_PRESUMIDO',
            sector='COMERCIO',
            current_tax_load=Decimal('5000.00'),
            reform_tax_load=Decimal('5000.00'),
            delta_value=Decimal('0.00'),
            impact_classification='NEUTRO'
        )
        
        # Dashboard do A deve mostrar faturamento médio de 10k (seu único registro)
        self.client.force_authenticate(user=self.user_a)
        url = reverse('simulation-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.data['faturamento_medio'], 10000.00)
        
        # Dashboard do B deve mostrar faturamento médio de 50k
        self.client.force_authenticate(user=self.user_b)
        response = self.client.get(url)
        self.assertEqual(response.data['faturamento_medio'], 50000.00)

class GenericAuthAndTests(APITestCase):
    # Manter testes básicos de sanidade
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="password123")
        self.client.force_authenticate(user=self.user)

    def test_simulation_endpoint_works(self):
        url = reverse('simulate')
        data = {
            "monthly_revenue": 10000.00,
            "costs": 2000.00,
            "tax_regime": "SIMPLES_NACIONAL",
            "sector": "SERVICOS"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificar se o log foi criado com o usuário correto
        self.assertEqual(SimulationLog.objects.last().user, self.user)