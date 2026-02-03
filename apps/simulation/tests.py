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

class ImpactAnalyzerTest(TestCase):
    def test_analyze_services_negative(self):
        analysis = ImpactAnalyzer.analyze(Decimal('1000.00'), Decimal('2000.00'), sector='SERVICOS')
        self.assertEqual(analysis['impact_classification'], 'NEGATIVO')
        self.assertIn("O setor de serviços tende a ser o mais impactado", analysis['suggestions'][0])
        self.assertIn("Servicos", analysis['message'])

    def test_analyze_commerce_positive(self):
        analysis = ImpactAnalyzer.analyze(Decimal('2000.00'), Decimal('1000.00'), sector='COMERCIO')
        self.assertEqual(analysis['impact_classification'], 'POSITIVO')
        self.assertIn("A redução da cumulatividade pode beneficiar sua cadeia", analysis['suggestions'][0])

    def test_analyze_with_uf(self):
        analysis = ImpactAnalyzer.analyze(Decimal('1000.00'), Decimal('1000.00'), sector='INDUSTRIA', uf='SP')
        self.assertEqual(analysis['impact_classification'], 'NEUTRO')
        self.assertIn("São Paulo", analysis['detalhes_setoriais'])

class SimulationAPITest(APITestCase):
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
        self.assertIn('sugestoes', response.data['analise'])
        self.assertIn('detalhes_setoriais', response.data['analise'])
        self.assertEqual(response.data['resumo_entrada']['estado'], 'SP')
        self.assertTrue(len(response.data['analise']['sugestoes']) >= 1)

    def test_simulation_endpoint_no_uf(self):
        url = reverse('simulate')
        data = {
            "monthly_revenue": 10000.00,
            "costs": 2000.00,
            "tax_regime": "LUCRO_PRESUMIDO",
            "sector": "INDUSTRIA"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['resumo_entrada']['estado'], 'Não informado')
