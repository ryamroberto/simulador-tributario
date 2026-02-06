from django.test import TestCase
from decimal import Decimal
from django.core.cache import cache
from simulation.services.calculator import TaxCalculator
from simulation.services.analyzer import ImpactAnalyzer
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from simulation.models import SimulationLog, TaxRule, SuggestionMatrix

class ManagementAPITest(APITestCase):
    """
    Testes de permissão e funcionalidade da API de gestão administrativa.
    """
    def setUp(self):
        cache.clear()
        # Usuário Comum
        self.common_user = User.objects.create_user(username="common", password="password123")
        # Usuário Admin
        self.admin_user = User.objects.create_user(username="admin", password="password123", is_staff=True)
        
        # Criar regra única para teste
        self.rule_name = "Regra Exclusiva de Teste"
        self.rule = TaxRule.objects.create(
            name=self.rule_name,
            rule_type="REFORMA",
            rate=Decimal('0.2650')
        )

    def test_common_user_forbidden(self):
        self.client.force_authenticate(user=self.common_user)
        url = reverse('tax-rules-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_list(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('tax-rules-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica se o registro criado está na resposta
        names = [item['name'] for item in response.data]
        self.assertIn(self.rule_name, names)

    def test_admin_user_can_update_rule(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('tax-rules-detail', kwargs={'pk': self.rule.pk})
        data = {"rate": "0.3000", "name": "Regra Alterada", "rule_type": "REFORMA"}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.rule.refresh_from_db()
        self.assertEqual(self.rule.rate, Decimal('0.3000'))

    def test_management_updates_invalidate_cache(self):
        # Chave correta conforme signals.py
        cache_key = f"tax_rate_{self.rule.rule_type}"
        cache.set(cache_key, Decimal('0.2650'))
        
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('tax-rules-detail', kwargs={'pk': self.rule.pk})
        # Alterar alíquota dispara Signal
        self.client.patch(url, {"rate": "0.3000"}, format='json')
        
        # Cache deve estar vazio para esta chave
        self.assertIsNone(cache.get(cache_key))

class OwnershipAPITest(APITestCase):
    def setUp(self):
        cache.clear()
        self.user_a = User.objects.create_user(username="usera", password="password123")
        self.user_b = User.objects.create_user(username="userb", password="password123")
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
        self.client.force_authenticate(user=self.user_b)
        url = reverse('simulation-history')
        response = self.client.get(url)
        self.assertEqual(len(response.data['results']), 0)

class GenericAuthAndTests(APITestCase):
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