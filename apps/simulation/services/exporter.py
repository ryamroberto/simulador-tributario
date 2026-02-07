import csv
from io import BytesIO, StringIO
from openpyxl import Workbook
from django.utils import timezone

class DataExporter:
    """
    Serviço para exportação de dados de simulação em formatos tabulares (CSV/Excel).
    """

    HEADERS = [
        "ID da Simulação", "Data de Criação", "Empresa", "Setor", 
        "Regime Tributário", "UF", "Faturamento Mensal (R$)", 
        "Custos Operacionais (R$)", "Carga Atual (R$)", 
        "Carga Reforma (R$)", "Diferença (Delta R$)", "Classificação de Impacto"
    ]

    @staticmethod
    def _prepare_rows(queryset):
        """
        Converte o queryset em uma lista de listas para os exportadores.
        """
        rows = []
        for log in queryset:
            rows.append([
                log.id,
                log.created_at.strftime('%d/%m/%Y %H:%M'),
                log.company.name if log.company else "Não Identificada",
                log.get_sector_display(),
                log.get_tax_regime_display(),
                log.state or "N/A",
                float(log.monthly_revenue),
                float(log.costs),
                float(log.current_tax_load),
                float(log.reform_tax_load),
                float(log.delta_value),
                log.get_impact_classification_display()
            ])
        return rows

    @classmethod
    def export_to_csv(cls, queryset):
        """
        Gera um buffer CSV com UTF-8 com BOM (para compatibilidade com Excel Windows).
        """
        buffer = StringIO()
        # Adicionar BOM para Excel reconhecer UTF-8
        buffer.write('\ufeff')
        
        writer = csv.writer(buffer, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(cls.HEADERS)
        writer.writerows(cls._prepare_rows(queryset))
        
        return BytesIO(buffer.getvalue().encode('utf-8'))

    @classmethod
    def export_to_excel(cls, queryset):
        """
        Gera um buffer Excel (.xlsx) usando openpyxl.
        """
        wb = Workbook()
        ws = wb.active
        ws.title = "Histórico de Simulações"

        # Adicionar Cabeçalhos
        ws.append(cls.HEADERS)

        # Adicionar Dados
        for row in cls._prepare_rows(queryset):
            ws.append(row)

        # Ajuste básico de largura de colunas
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column].width = adjusted_width

        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        return buffer
