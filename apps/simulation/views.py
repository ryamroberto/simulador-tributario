from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
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

class SimulationDashboardView(APIView):
    """
    Endpoint que fornece métricas consolidadas do histórico de simulações.
    """
    
    @extend_schema(
        summary="Obter Métricas do Dashboard",
        description="Retorna estatísticas agregadas de todas as simulações realizadas para análise macro.",
        tags=['Simulação']
    )
    def get(self, request, *args, **kwargs):
        # Agregações básicas
        aggregates = SimulationLog.objects.aggregate(
            total=Count('id'),
            faturamento_medio=Avg('monthly_revenue'),
            carga_atual_media=Avg('current_tax_load'),
            carga_reforma_media=Avg('reform_tax_load')
        )
        
        # Distribuição de impacto
        impact_dist = SimulationLog.objects.values('impact_classification').annotate(
            total=Count('id')
        ).order_by('-total')
        
        # Top 3 setores
        top_setores = SimulationLog.objects.values('sector').annotate(
            total=Count('id')
        ).order_by('-total')[:3]
        
        # Formatando resposta
        data = {
            "total_simulacoes": aggregates['total'] or 0,
            "faturamento_medio": round(aggregates['faturamento_medio'] or 0, 2),
            "comparativo_carga_media": {
                "carga_atual_media": round(aggregates['carga_atual_media'] or 0, 2),
                "carga_reforma_media": round(aggregates['carga_reforma_media'] or 0, 2)
            },
            "distribuicao_impacto": {
                item['impact_classification']: item['total'] for item in impact_dist
            },
            "top_setores": [
                {
                    "setor": item['sector'],
                    "total": item['total']
                } for item in top_setores
            ]
        }
        
        return Response(data, status=status.HTTP_200_OK)
