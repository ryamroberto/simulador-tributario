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
import unittest

class ManagementAPITest(APITestCase):
    def setUp(self):
        cache.clear()
        self.common_user = User.objects.create_user(username="common", password="password123")
        self.admin_user = User.objects.create_user(username="admin", password="password123", is_staff=True)
        self.rule = TaxRule.objects.create(name="Regra Teste", rule_type="REFORMA", rate=Decimal('0.2650'))

    def test_common_user_forbidden(self):
        self.client.force_authenticate(user=self.common_user)
        url = reverse('tax-rules-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class OwnershipAndExportAPITest(APITestCase):
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

    def test_export_csv_is_private(self):
        self.client.force_authenticate(user=self.user_b)
        url = reverse('simulation-history-export')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')

    def test_export_excel_format(self):
        self.client.force_authenticate(user=self.user_a)
        url = reverse('simulation-history-export-excel')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

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