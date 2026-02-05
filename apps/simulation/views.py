from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from .serializers import SimulationInputSerializer, SimulationLogListSerializer
from .services.calculator import TaxCalculator
from .services.analyzer import ImpactAnalyzer
from .models import SimulationLog

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

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

            # Salvar Log de Simulação
            SimulationLog.objects.create(
                company_id=data.get('company_id'),
                monthly_revenue=data['monthly_revenue'],
                costs=data['costs'],
                tax_regime=data['tax_regime'],
                sector=data['sector'],
                state=data.get('state'),
                current_tax_load=current_tax,
                reform_tax_load=reform_tax,
                delta_value=analysis['delta_value'],
                impact_classification=analysis['impact_classification']
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

class SimulationHistoryView(ListAPIView):
    """
    Endpoint para listar o histórico de simulações realizadas.
    Permite filtrar por empresa e retorna os dados paginados.
    """
    queryset = SimulationLog.objects.all()
    serializer_class = SimulationLogListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company']

    @extend_schema(
        summary="Listar Histórico de Simulações",
        description="Retorna uma lista paginada de todas as simulações gravadas no sistema. Pode ser filtrado por ID da empresa.",
        tags=['Simulação']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)