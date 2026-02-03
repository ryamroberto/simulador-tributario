from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Company

class CompanyModelTest(TestCase):
    def test_create_company(self):
        company = Company.objects.create(
            name="Empresa Teste",
            monthly_revenue=10000.00,
            sector=Company.Sector.SERVICES,
            state=Company.UF.SP,
            tax_regime=Company.TaxRegime.SIMPLES_NACIONAL
        )
        self.assertEqual(str(company), "Empresa Teste")
        self.assertEqual(company.state, "SP")

class CompanyAPITest(APITestCase):
    def test_create_company_api(self):
        url = reverse('company-list')
        data = {
            "name": "Nova Empresa",
            "monthly_revenue": 50000.00,
            "sector": "SERVICOS",
            "state": "RJ",
            "tax_regime": "LUCRO_PRESUMIDO"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, "Nova Empresa")

    def test_invalid_revenue_api(self):
        url = reverse('company-list')
        data = {
            "name": "Empresa Invalida",
            "monthly_revenue": -100.00,
            "sector": "SERVICOS",
            "state": "SP",
            "tax_regime": "SIMPLES_NACIONAL"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if message is in PT-BR
        self.assertIn("O faturamento mensal deve ser maior que zero.", str(response.data))