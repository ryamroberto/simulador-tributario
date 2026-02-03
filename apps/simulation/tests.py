from django.test import TestCase
from decimal import Decimal
from apps.simulation.services.calculator import TaxCalculator
from apps.simulation.services.analyzer import ImpactAnalyzer
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class TaxCalculatorTest(TestCase):
    def test_calculate_simples_nacional(self):
        company_data = {'tax_regime': 'SIMPLES_NACIONAL'}
        financials = {'monthly_revenue': Decimal('10000.00')}
        tax = TaxCalculator.calculate_current_tax(company_data, financials)
        self.assertEqual(tax, Decimal('1000.00')) # 10% de 10000

    def test_calculate_lucro_presumido(self):
        company_data = {'tax_regime': 'LUCRO_PRESUMIDO'}
        financials = {'monthly_revenue': Decimal('10000.00')}
        tax = TaxCalculator.calculate_current_tax(company_data, financials)
        # LP_PIS (0.0065) + LP_COFINS (0.03) + LP_ISS (0.05) + LP_IRPJ (0.048) + LP_CSLL (0.0288) = 0.1633
        self.assertEqual(tax, Decimal('1633.00'))

    def test_calculate_reform(self):
        company_data = {} # Regime não importa para reforma nesta lógica
        financials = {
            'monthly_revenue': Decimal('10000.00'),
            'costs': Decimal('2000.00')
        }
        tax = TaxCalculator.calculate_reform_tax(company_data, financials)
        # (10000 - 2000) * 0.265 = 8000 * 0.265 = 2120
        self.assertEqual(tax, Decimal('2120.00'))

class SimulationAPITest(APITestCase):
    def test_simulation_endpoint(self):
        url = reverse('simulate')
        data = {
            "monthly_revenue": 10000.00,
            "costs": 2000.00,
            "tax_regime": "SIMPLES_NACIONAL",
            "sector": "SERVICOS"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('carga_tributaria_atual', str(response.data))
        self.assertIn('carga_tributaria_reforma', str(response.data))
        # Verificar se está em PT-BR
        self.assertEqual(response.data['analise']['classificacao_impacto'], 'NEGATIVO')