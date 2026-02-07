from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Company

class CompanyModelTest(TestCase):
    def test_create_company(self):
        company = Company.objects.create(
            name="Empresa Teste",
            cnpj="11.222.333/0001-81",
            monthly_revenue=10000.00,
            sector=Company.Sector.SERVICES,
            state=Company.UF.SP,
            tax_regime=Company.TaxRegime.SIMPLES_NACIONAL
        )
        self.assertEqual(str(company), "Empresa Teste")
        self.assertEqual(company.cnpj, "11.222.333/0001-81")

from django.contrib.auth.models import User

class CompanyAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="password123")
        self.client.force_authenticate(user=self.user)

    def test_create_company_api(self):
        url = reverse('company-list')
        data = {
            "name": "Nova Empresa",
            "cnpj": "11.222.333/0001-81",
            "monthly_revenue": 50000.00,
            "sector": "SERVICOS",
            "state": "RJ",
            "tax_regime": "LUCRO_PRESUMIDO"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)

    def test_invalid_cnpj_api(self):
        url = reverse('company-list')
        data = {
            "name": "Empresa CNPJ Invalido",
            "cnpj": "11.111.111/1111-11", # CNPJ inválido por dígitos repetidos
            "monthly_revenue": 50000.00,
            "sector": "SERVICOS",
            "state": "SP",
            "tax_regime": "SIMPLES_NACIONAL"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("CNPJ inválido", str(response.data))

    def test_invalid_revenue_api(self):
        url = reverse('company-list')
        data = {
            "name": "Empresa Invalida",
            "cnpj": "11.222.333/0001-81",
            "monthly_revenue": -100.00,
            "sector": "SERVICOS",
            "state": "SP",
            "tax_regime": "SIMPLES_NACIONAL"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)