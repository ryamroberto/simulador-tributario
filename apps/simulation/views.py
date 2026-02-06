from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from django.http import FileResponse
from drf_spectacular.utils import extend_schema
from .serializers import SimulationInputSerializer, SimulationLogListSerializer
from .services.calculator import TaxCalculator
from .services.analyzer import ImpactAnalyzer
from .services.pdf_generator import PDFGenerator
from .models import SimulationLog

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SimulationView(APIView):
    """
    Endpoint para executar a simulação de impacto tributário vinculada ao usuário.
    """
    serializer_class = SimulationInputSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Executar Simulação",
        description="Calcula o impacto da reforma tributária e salva um log vinculado ao seu usuário.",
        request=SimulationInputSerializer,
        tags=['Simulações']
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
            
            # Analisar Impacto
            analysis = ImpactAnalyzer.analyze(
                current_tax, 
                reform_tax, 
                sector=data['sector'],
                uf=data.get('state')
            )

            # Salvar Log vinculado ao usuário
            SimulationLog.objects.create(
                user=request.user,
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
            
            # Resposta
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
    Endpoint para listar apenas o histórico do usuário autenticado.
    """
    serializer_class = SimulationLogListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company']

    def get_queryset(self):
        return SimulationLog.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Listar Histórico",
        description="Retorna o seu histórico pessoal de simulações.",
        tags=['Simulações']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class SimulationDashboardView(APIView):
    """
    Endpoint que fornece métricas baseadas apenas nos logs do usuário.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Obter Dashboard de Métricas",
        description="Retorna estatísticas baseadas exclusivamente nas suas simulações.",
        tags=['Simulações']
    )
    def get(self, request, *args, **kwargs):
        # Filtro por usuário nas agregações
        user_logs = SimulationLog.objects.filter(user=request.user)
        
        aggregates = user_logs.aggregate(
            total=Count('id'),
            faturamento_medio=Avg('monthly_revenue'),
            carga_atual_media=Avg('current_tax_load'),
            carga_reforma_media=Avg('reform_tax_load')
        )
        
        impact_dist = user_logs.values('impact_classification').annotate(
            total=Count('id')
        ).order_by('-total')
        
        top_setores = user_logs.values('sector').annotate(
            total=Count('id')
        ).order_by('-total')[:3]
        
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

class SimulationExportPDFView(APIView):
    """
    Endpoint para exportar uma simulação própria para PDF.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Exportar para PDF",
        description="Gera um PDF para uma simulação sua.",
        tags=['Simulações']
    )
    def get(self, request, pk, *args, **kwargs):
        # get_object_or_404 com filtro de usuário garante segurança
        log = get_object_or_404(SimulationLog, pk=pk, user=request.user)
        pdf_buffer = PDFGenerator.generate_simulation_report(log)
        
        return FileResponse(
            pdf_buffer,
            as_attachment=True,
            filename=f"relatorio_simulacao_{log.id}.pdf",
            content_type='application/pdf'
        )
