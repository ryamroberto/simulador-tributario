from django.test import TestCase
from decimal import Decimal
from django.core.cache import cache
from simulation.services.calculator import TaxCalculator
from simulation.services.analyzer import ImpactAnalyzer
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class TaxCalculatorTest(TestCase):
    def setUp(self):
        cache.clear()

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
    def setUp(self):
        cache.clear()

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
    def setUp(self):
        cache.clear()

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

    def test_costs_exceed_revenue(self):
        url = reverse('simulate')
        data = {
            "monthly_revenue": 10000.00,
            "costs": 15000.00, # Custos maiores que faturamento
            "tax_regime": "SIMPLES_NACIONAL",
            "sector": "SERVICOS"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("costs", response.data)
        self.assertIn("não podem ser maiores que o faturamento", str(response.data['costs']))

    def test_simulation_log_creation(self):
        from simulation.models import SimulationLog
        url = reverse('simulate')
        data = {
            "monthly_revenue": 10000.00,
            "costs": 2000.00,
            "tax_regime": "SIMPLES_NACIONAL",
            "sector": "SERVICOS",
            "state": "SP"
        }
        initial_count = SimulationLog.objects.count()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SimulationLog.objects.count(), initial_count + 1)
        
        log = SimulationLog.objects.last()
        self.assertEqual(log.monthly_revenue, Decimal('10000.00'))
        self.assertEqual(log.impact_classification, response.data['analise']['classificacao_impacto'])

class SimulationHistoryAPITest(APITestCase):
    def setUp(self):
        from simulation.models import SimulationLog
        from companies.models import Company
        cache.clear()
        
        # Criar empresa para teste de filtro
        self.company = Company.objects.create(
            name="Empresa Teste",
            cnpj="12345678000199",
            monthly_revenue=Decimal('10000.00'),
            tax_regime="LUCRO_PRESUMIDO",
            sector="SERVICOS",
            state="SP"
        )
        
        # Criar logs
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
        
        SimulationLog.objects.create(
            company=None,
            monthly_revenue=Decimal('50000.00'),
            costs=Decimal('10000.00'),
            tax_regime='SIMPLES_NACIONAL',
            sector='COMERCIO',
            state='RJ',
            current_tax_load=Decimal('5000.00'),
            reform_tax_load=Decimal('10600.00'),
            delta_value=Decimal('5600.00'),
            impact_classification='NEGATIVO'
        )

    def test_list_history(self):
        url = reverse('simulation-history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response.data contém 'results' devido à paginação
        data = response.data['results']
        self.assertEqual(len(data), 2)
        self.assertIn('regime_tributario_desc', data[0])
        self.assertIn('data_criacao', data[0])

    def test_filter_by_company(self):
        url = reverse('simulation-history')
        response = self.client.get(f"{url}?company={self.company.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['company'], self.company.id)

    def test_pt_br_descriptions(self):
        url = reverse('simulation-history')
        response = self.client.get(url)
        data = response.data['results']
        
        # Encontrar o registro do Simples Nacional
        simples_log = next(item for item in data if item['tax_regime'] == 'SIMPLES_NACIONAL')
        self.assertEqual(simples_log['regime_tributario_desc'], 'Simples Nacional')
        self.assertEqual(simples_log['impacto_desc'], 'Negativo')

class SimulationDashboardAPITest(APITestCase):
    def setUp(self):
        from simulation.models import SimulationLog
        cache.clear()
        
        # Criar massa de dados variada
        # Registro 1: Serviços, Positivo
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
        # Registro 2: Serviços, Negativo
        SimulationLog.objects.create(
            monthly_revenue=Decimal('20000.00'),
            costs=Decimal('2000.00'),
            tax_regime='SIMPLES_NACIONAL',
            sector='SERVICOS',
            current_tax_load=Decimal('2000.00'),
            reform_tax_load=Decimal('4770.00'),
            delta_value=Decimal('2770.00'),
            impact_classification='NEGATIVO'
        )
        # Registro 3: Comércio, Neutro
        SimulationLog.objects.create(
            monthly_revenue=Decimal('30000.00'),
            costs=Decimal('10000.00'),
            tax_regime='LUCRO_PRESUMIDO',
            sector='COMERCIO',
            current_tax_load=Decimal('4899.00'),
            reform_tax_load=Decimal('4899.00'),
            delta_value=Decimal('0.00'),
            impact_classification='NEUTRO'
        )

    def test_dashboard_metrics(self):
        url = reverse('simulation-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data
        self.assertEqual(data['total_simulacoes'], 3)
        # Média faturamento: (10k + 20k + 30k) / 3 = 20k
        self.assertEqual(Decimal(str(data['faturamento_medio'])), Decimal('20000.00'))
        
        # Distribuição impacto
        self.assertEqual(data['distribuicao_impacto']['POSITIVO'], 1)
        self.assertEqual(data['distribuicao_impacto']['NEGATIVO'], 1)
        self.assertEqual(data['distribuicao_impacto']['NEUTRO'], 1)
        
        # Top setores
        self.assertEqual(data['top_setores'][0]['setor'], 'SERVICOS')
        self.assertEqual(data['top_setores'][0]['total'], 2)
        self.assertEqual(data['top_setores'][1]['setor'], 'COMERCIO')
        self.assertEqual(data['top_setores'][1]['total'], 1)

class SimulationExportAPITest(APITestCase):
    def setUp(self):
        from simulation.models import SimulationLog
        cache.clear()
        
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
        self.assertIn('attachment', response['Content-Disposition'])
        self.assertIn(f'relatorio_simulacao_{self.log.id}.pdf', response['Content-Disposition'])
        
        # Para FileResponse, verificamos se há conteúdo no stream
        content = b"".join(response.streaming_content)
        self.assertTrue(len(content) > 0)
