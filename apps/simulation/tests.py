from django.test import TestCase
from decimal import Decimal
from django.core.cache import cache
from simulation.services.calculator import TaxCalculator
from simulation.services.analyzer import ImpactAnalyzer
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

class TaxCalculatorTest(TestCase):
    def setUp(self):
        cache.clear()

    def test_calculate_simples_nacional(self):
        company_data = {'tax_regime': 'SIMPLES_NACIONAL'}
        financials = {'monthly_revenue': Decimal('10000.00')}
        tax = TaxCalculator.calculate_current_tax(company_data, financials)
        self.assertEqual(tax, Decimal('1000.00'))

    def test_calculate_lucro_presumido(self):
        company_data = {'tax_regime': 'LUCRO_PRESUMIDO'}
        financials = {'monthly_revenue': Decimal('10000.00')}
        tax = TaxCalculator.calculate_current_tax(company_data, financials)
        self.assertEqual(tax, Decimal('1633.00'))

class AuthAPITest(APITestCase):
    def test_user_registration(self):
        url = reverse('user_register')
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "password_confirm": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_and_token_obtain(self):
        User.objects.create_user(username="testuser", password="password123")
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {"username": "testuser", "password": "password123"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class SimulationAPITest(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username="apiuser", password="password123")
        self.client.force_authenticate(user=self.user)

    def test_simulation_endpoint_full(self):
        url = reverse('simulate')
        data = {
            "monthly_revenue": 10000.00,
            "costs": 2000.00,
            "tax_regime": "SIMPLES_NACIONAL",
            "sector": "SERVICOS",
            "state": "SP"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class SimulationHistoryAPITest(APITestCase):
    def setUp(self):
        from simulation.models import SimulationLog
        from companies.models import Company
        cache.clear()
        self.user = User.objects.create_user(username="historyuser", password="password123")
        self.client.force_authenticate(user=self.user)
        
        self.company = Company.objects.create(
            name="Empresa Teste",
            cnpj="12345678000199",
            monthly_revenue=Decimal('10000.00'),
            tax_regime="LUCRO_PRESUMIDO",
            sector="SERVICOS",
            state="SP"
        )
        
        SimulationLog.objects.create(
            company=self.company,
            monthly_revenue=Decimal('10000.00'),
            costs=Decimal('2000.00'),
            tax_regime='LUCRO_PRESUMIDO',
            sector='SERVICOS',
            state='SP',
            current_tax_load=Decimal('1633.00'),
            reform_tax_load=Decimal('2120.00'),
            delta_value=Decimal('487.00'),
            impact_classification='NEGATIVO'
        )

    def test_list_history(self):
        url = reverse('simulation-history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class SimulationDashboardAPITest(APITestCase):
    def setUp(self):
        from simulation.models import SimulationLog
        cache.clear()
        self.user = User.objects.create_user(username="dashuser", password="password123")
        self.client.force_authenticate(user=self.user)
        
        SimulationLog.objects.create(
            monthly_revenue=Decimal('10000.00'),
            costs=Decimal('5000.00'),
            tax_regime='LUCRO_PRESUMIDO',
            sector='SERVICOS',
            current_tax_load=Decimal('1633.00'),
            reform_tax_load=Decimal('1325.00'),
            delta_value=Decimal('-308.00'),
            impact_classification='POSITIVO'
        )

    def test_dashboard_metrics(self):
        url = reverse('simulation-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class SimulationExportAPITest(APITestCase):
    def setUp(self):
        from simulation.models import SimulationLog
        cache.clear()
        self.user = User.objects.create_user(username="exportuser", password="password123")
        self.client.force_authenticate(user=self.user)
        
        self.log = SimulationLog.objects.create(
            monthly_revenue=Decimal('10000.00'),
            costs=Decimal('5000.00'),
            tax_regime='LUCRO_PRESUMIDO',
            sector='SERVICOS',
            current_tax_load=Decimal('1633.00'),
            reform_tax_load=Decimal('1325.00'),
            delta_value=Decimal('-308.00'),
            impact_classification='POSITIVO'
        )

    def test_export_pdf_endpoint(self):
        url = reverse('simulation-export-pdf', kwargs={'pk': self.log.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')
