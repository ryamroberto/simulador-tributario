from django.db import migrations
from decimal import Decimal

def populate_data(apps, schema_editor):
    TaxRule = apps.get_model('simulation', 'TaxRule')
    SuggestionMatrix = apps.get_model('simulation', 'SuggestionMatrix')

    # 1. Popular TaxRules
    TaxRule.objects.create(
        name="Simples Nacional - Alíquota Média",
        rule_type='SIMPLES_NACIONAL',
        rate=Decimal('0.1000')
    )
    
    # Para o Lucro Presumido, o código antigo somava várias alíquotas.
    # Vamos criar uma regra única consolidada para o MVP.
    # LP_PIS(0.0065) + LP_COFINS(0.03) + LP_ISS(0.05) + LP_IRPJ(0.048) + LP_CSLL(0.0288) = 0.1633
    TaxRule.objects.create(
        name="Lucro Presumido - Carga Consolidada (PIS/COFINS/ISS/IR/CS)",
        rule_type='LUCRO_PRESUMIDO',
        rate=Decimal('0.1633')
    )

    TaxRule.objects.create(
        name="Reforma Tributária - IBS/CBS Estimado",
        rule_type='REFORMA',
        rate=Decimal('0.2650')
    )

    # 2. Popular SuggestionMatrix
    sugestoes = {
        'SERVICOS': {
            'NEGATIVO': [
                "O setor de serviços tende a ser o mais impactado pela alíquota única do IBS/CBS. Revise sua margem de lucro.",
                "Considere a renegociação de contratos de longo prazo prevendo o aumento da carga sobre o faturamento.",
                "Avalie a possibilidade de retenção de créditos sobre insumos, que passará a ser permitida de forma ampla."
            ],
            'POSITIVO': [
                "A simplificação tributária pode reduzir custos administrativos significativos para sua prestação de serviço.",
                "Aproveite a desoneração de investimentos em tecnologia para otimizar sua operação.",
                "Com a redução da carga, avalie repassar o ganho para o preço final para ganhar competitividade."
            ],
            'NEUTRO': [
                "Mantenha o monitoramento das leis complementares que definirão as alíquotas específicas do seu subsetor.",
                "Prepare seu sistema de faturamento para o novo modelo de IVA (IBS/CBS).",
                "Acompanhe o período de transição para ajustar o fluxo de caixa conforme os novos vencimentos."
            ]
        },
        'COMERCIO': {
            'NEGATIVO': [
                "Analise o impacto no preço de venda, especialmente em itens com margens reduzidas.",
                "Verifique se seus fornecedores estão adaptados ao novo regime para garantir a integridade dos créditos.",
                "O fluxo de caixa pode ser afetado pela mudança no momento do fato gerador do imposto."
            ],
            'POSITIVO': [
                "A redução da cumulatividade pode beneficiar sua cadeia de suprimentos.",
                "Menos burocracia na circulação de mercadorias entre estados deve facilitar sua logística.",
                "Avalie a expansão para novos mercados regionais aproveitando a alíquota única nacional."
            ],
            'NEUTRO': [
                "Certifique-se de que sua precificação considera a mudança na composição dos impostos (IBS/CBS).",
                "Monitore as mudanças nas regras de crédito para mercadorias em estoque durante a transição.",
                "Mantenha o cadastro de produtos atualizado para evitar erros na aplicação das novas alíquotas."
            ]
        },
        'INDUSTRIA': {
            'NEGATIVO': [
                "Grandes investimentos em ativos fixos devem ser planejados considerando o novo modelo de aproveitamento de créditos.",
                "Revise os custos de matérias-primas e o impacto da extinção do IPI em sua cadeia.",
                "Avalie o impacto nos incentivos regionais existentes que podem ser extintos ou modificados."
            ],
            'POSITIVO': [
                "A desoneração total de exportações e investimentos deve impulsionar sua competitividade internacional.",
                "A não-cumulatividade plena permitirá recuperar impostos pagos em praticamente todos os insumos.",
                "A extinção do IPI simplificará drasticamente seu controle fiscal e obrigações acessórias."
            ],
            'NEUTRO': [
                "Planeje a transição tecnológica de seus sistemas de ERP para suportar o cálculo do IVA.",
                "Fique atento às regras de transição para o uso de créditos acumulados do regime antigo.",
                "Acompanhe as definições sobre o Imposto Seletivo que pode incidir sobre determinados produtos."
            ]
        }
    }

    for setor, impactos in sugestoes.items():
        for impacto, textos in impactos.items():
            for texto in textos:
                SuggestionMatrix.objects.create(
                    sector=setor,
                    impact=impacto,
                    suggestion_text=texto
                )

def rollback_data(apps, schema_editor):
    TaxRule = apps.get_model('simulation', 'TaxRule')
    SuggestionMatrix = apps.get_model('simulation', 'SuggestionMatrix')
    TaxRule.objects.all().delete()
    SuggestionMatrix.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('simulation', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_data, rollback_data),
    ]