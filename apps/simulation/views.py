from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from django.http import FileResponse
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework.throttling import ScopedRateThrottle
from .serializers import (
    SimulationInputSerializer, 
    SimulationLogListSerializer,
    TaxRuleSerializer,
    SuggestionMatrixSerializer
)
from .services.calculator import TaxCalculator
from .services.analyzer import ImpactAnalyzer
from .services.pdf_generator import PDFGenerator
from .services.exporter import DataExporter
from .models import SimulationLog, TaxRule, SuggestionMatrix

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SimulationView(APIView):
    serializer_class = SimulationInputSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = SimulationInputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            company_data = {
                'tax_regime': data['tax_regime'],
                'sector': data['sector'],
                'state': data.get('state')
            }
            financials = {
                'monthly_revenue': data['monthly_revenue'],
                'costs': data['costs']
            }
            current_tax = TaxCalculator.calculate_current_tax(company_data, financials)
            reform_tax = TaxCalculator.calculate_reform_tax(company_data, financials)
            analysis = ImpactAnalyzer.analyze(
                current_tax, 
                reform_tax, 
                sector=data['sector'],
                uf=data.get('state')
            )
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
    serializer_class = SimulationLogListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company']

    def get_queryset(self):
        return SimulationLog.objects.filter(user=self.request.user)

class SimulationDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user_logs = SimulationLog.objects.filter(user=request.user)
        aggregates = user_logs.aggregate(
            total=Count('id'),
            faturamento_medio=Avg('monthly_revenue'),
            carga_atual_media=Avg('current_tax_load'),
            carga_reforma_media=Avg('reform_tax_load')
        )
        impact_dist = user_logs.values('impact_classification').annotate(total=Count('id')).order_by('-total')
        top_setores = user_logs.values('sector').annotate(total=Count('id')).order_by('-total')[:3]
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
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'export'
    def get(self, request, pk, *args, **kwargs):
        log = get_object_or_404(SimulationLog, pk=pk, user=request.user)
        pdf_buffer = PDFGenerator.generate_simulation_report(log)
        return FileResponse(pdf_buffer, as_attachment=True, filename=f"relatorio_simulacao_{log.id}.pdf", content_type='application/pdf')

class SimulationHistoryExportView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'export'
    def get(self, request, *args, **kwargs):
        queryset = SimulationLog.objects.filter(user=request.user).order_by('-created_at')
        export_format = request.query_params.get('format', 'csv').lower()

        # Verificar se a URL indica exportação em Excel (para compatibilidade com testes)
        if request.path.endswith('/excel/') or export_format == 'excel':
            export_format = 'excel'

        timestamp = timezone.now().strftime('%Y%m%d')

        if export_format == 'excel':
            buffer = DataExporter.export_to_excel(queryset)
            filename = f"historico_simulacoes_{timestamp}.xlsx"
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        else:
            buffer = DataExporter.export_to_csv(queryset)
            filename = f"historico_simulacoes_{timestamp}.csv"
            content_type = 'text/csv'

        return FileResponse(
            buffer,
            as_attachment=True,
            filename=filename,
            content_type=content_type
        )

class TaxRuleViewSet(viewsets.ModelViewSet):
    queryset = TaxRule.objects.all()
    serializer_class = TaxRuleSerializer
    permission_classes = [IsAdminUser]

class SuggestionMatrixViewSet(viewsets.ModelViewSet):
    queryset = SuggestionMatrix.objects.all()
    serializer_class = SuggestionMatrixSerializer
    permission_classes = [IsAdminUser]