from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import cm

class PDFGenerator:
    """
    Serviço especializado na geração de relatórios de impacto tributário em formato PDF.
    """

    @staticmethod
    def generate_simulation_report(simulation_log):
        """
        Gera um buffer de bytes contendo o PDF da simulação.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        elements = []
        styles = getSampleStyleSheet()
        
        # Estilos Customizados
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            alignment=1, # Center
            spaceAfter=20
        )
        
        section_style = ParagraphStyle(
            'SectionStyle',
            parent=styles['Heading2'],
            spaceBefore=15,
            spaceAfter=10
        )

        # Cabeçalho
        elements.append(Paragraph("Relatório de Impacto da Reforma Tributária", title_style))
        elements.append(Paragraph(f"Simulação ID: {simulation_log.id}", styles['Normal']))
        elements.append(Paragraph(f"Data: {simulation_log.created_at.strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 1*cm))

        # Dados da Empresa
        elements.append(Paragraph("Resumo dos Dados de Entrada", section_style))
        empresa_nome = simulation_log.company.name if simulation_log.company else "Não Identificada"
        
        data_entrada = [
            ["Empresa:", empresa_nome],
            ["Regime Tributário Atual:", simulation_log.get_tax_regime_display()],
            ["Setor de Atuação:", simulation_log.get_sector_display()],
            ["UF:", simulation_log.state or "Não informada"],
            ["Faturamento Mensal:", f"R$ {simulation_log.monthly_revenue:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")],
            ["Custos Operacionais:", f"R$ {simulation_log.costs:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")]
        ]
        
        t_entrada = Table(data_entrada, colWidths=[6*cm, 10*cm])
        t_entrada.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(t_entrada)
        elements.append(Spacer(1, 1*cm))

        # Comparativo Financeiro
        elements.append(Paragraph("Comparativo de Carga Tributária", section_style))
        
        data_comparativo = [
            ["Cenário", "Carga Mensal (R$)"],
            ["Atual (Antes da Reforma)", f"R$ {simulation_log.current_tax_load:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")],
            ["Proposta (Pós-Reforma)", f"R$ {simulation_log.reform_tax_load:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")],
            ["Diferença (Delta)", f"R$ {simulation_log.delta_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")]
        ]
        
        t_comp = Table(data_comparativo, colWidths=[8*cm, 8*cm])
        
        # Cor baseada no impacto
        delta_color = colors.black
        if simulation_log.impact_classification == 'NEGATIVO':
            delta_color = colors.red
        elif simulation_log.impact_classification == 'POSITIVO':
            delta_color = colors.green

        t_comp.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('TEXTCOLOR', (1, 3), (1, 3), delta_color),
            ('FONTNAME', (0, 3), (1, 3), 'Helvetica-Bold'),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(t_comp)
        elements.append(Spacer(1, 1*cm))

        # Análise Qualitativa
        elements.append(Paragraph("Análise e Sugestões", section_style))
        impacto_text = f"Classificação de Impacto: <b>{simulation_log.get_impact_classification_display()}</b>"
        elements.append(Paragraph(impacto_text, styles['Normal']))
        elements.append(Spacer(1, 0.5*cm))
        
        elements.append(Paragraph("<b>Observações:</b>", styles['Normal']))
        obs = "O resultado acima é uma estimativa baseada nas alíquotas padrão da reforma tributária (IBS/CBS)."
        elements.append(Paragraph(obs, styles['Normal']))

        # Gerar PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
