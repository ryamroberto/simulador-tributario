from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import SimulationInputSerializer
from .services.calculator import TaxCalculator
from .services.analyzer import ImpactAnalyzer

class SimulationView(APIView):
    """
    Endpoint para executar a simulação de impacto tributário com feedbacks detalhados.
    """
    serializer_class = SimulationInputSerializer
    
    @extend_schema(
        summary="Executar Simulação Tributária",
        description="Calcula o impacto da reforma tributária comparando a carga atual com a proposta (IBS/CBS) e fornece sugestões baseadas no setor.",
        request=SimulationInputSerializer,
        tags=['Simulação']
    )
    def post(self, request, *args, **kwargs):
        serializer = SimulationInputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Preparar dados para o calculador
            company_data = {
                'tax_regime': data['tax_regime'],
                'sector': data['sector'],
                'state': data.get('state')
            }
            financials = {
                'monthly_revenue': data['monthly_revenue'],
                'costs': data['costs']
            }
            
            # Executar Cálculos
            current_tax = TaxCalculator.calculate_current_tax(company_data, financials)
            reform_tax = TaxCalculator.calculate_reform_tax(company_data, financials)
            
            # Analisar Impacto com sugestões dinâmicas
            analysis = ImpactAnalyzer.analyze(
                current_tax, 
                reform_tax, 
                sector=data['sector'],
                uf=data.get('state')
            )
            
            # Montar Resposta em PT-BR
            response_data = {
                'resumo_entrada': {
                    'faturamento': data['monthly_revenue'],
                    'custos': data['costs'],
                    'regime_atual': data['tax_regime'],
                    'setor': data['sector'],
                    'estado': data.get('state', 'Não informado')
                },
                'resultados': {
                    'carga_tributaria_atual': current_tax.quantize(TaxCalculator.SN_AVERAGE_RATE),
                    'carga_tributaria_reforma': reform_tax.quantize(TaxCalculator.REFORM_RATE),
                    'diferenca_absoluta': analysis['delta_value'].quantize(TaxCalculator.SN_AVERAGE_RATE),
                    'diferenca_percentual': analysis['delta_percentage']
                },
                'analise': {
                    'classificacao_impacto': analysis['impact_classification'],
                    'mensagem': analysis['message'],
                    'detalhes_setoriais': analysis['detalhes_setoriais'],
                    'sugestoes': analysis['suggestions']
                }
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)