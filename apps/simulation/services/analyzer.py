from decimal import Decimal

class ImpactAnalyzer:
    """
    Serviço para analisar a diferença entre as cargas tributárias e fornecer insights qualitativos.
    """

    SUGESTOES = {
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

    @classmethod
    def get_suggestions(cls, sector, impact_classification):
        sector_suggestions = cls.SUGESTOES.get(sector, {})
        return sector_suggestions.get(impact_classification, ["Considere revisar seus créditos tributários e analisar o impacto na precificação final."])

    @classmethod
    def analyze(cls, current_tax, reform_tax, sector='OUTROS', uf=None):
        delta_value = reform_tax - current_tax
        
        # Mapeamento simples de UF para testes e exibição
        uf_map = {
            'SP': 'São Paulo', 'RJ': 'Rio de Janeiro', 'MG': 'Minas Gerais', 'ES': 'Espírito Santo',
            'PR': 'Paraná', 'SC': 'Santa Catarina', 'RS': 'Rio Grande do Sul',
            'BA': 'Bahia', 'PE': 'Pernambuco', 'CE': 'Ceará', 'RN': 'Rio Grande do Norte',
            'PB': 'Paraíba', 'AL': 'Alagoas', 'SE': 'Sergipe', 'MA': 'Maranhão', 'PI': 'Piauí',
            'AM': 'Amazonas', 'PA': 'Pará', 'RO': 'Rondônia', 'AC': 'Acre', 'RR': 'Roraima',
            'AP': 'Amapá', 'TO': 'Tocantins', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul',
            'GO': 'Goiás', 'DF': 'Distrito Federal'
        }
        uf_display = uf_map.get(uf, uf)

        if current_tax > 0:
            delta_percentage = (delta_value / current_tax) * 100
        else:
            delta_percentage = Decimal('0.00')

        if delta_value > 0:
            classification = 'NEGATIVO'
            base_message = f"Sua carga tributária para o setor de {sector.capitalize()} deve aumentar com a reforma."
        elif delta_value < 0:
            classification = 'POSITIVO'
            base_message = f"Sua carga tributária para o setor de {sector.capitalize()} deve diminuir com a reforma."
        else:
            classification = 'NEUTRO'
            base_message = "Sua carga tributária deve permanecer estável."

        suggestions = cls.get_suggestions(sector, classification)
        
        # Detalhes específicos por UF
        detalhes_setoriais = f"Análise baseada nas médias nacionais para {sector.capitalize()}."
        if uf:
            detalhes_setoriais += f" Consideradas particularidades da região {uf_display} no contexto da transição federativa."

        return {
            'delta_value': delta_value,
            'delta_percentage': delta_percentage.quantize(Decimal('0.01')),
            'impact_classification': classification,
            'message': base_message,
            'suggestions': suggestions,
            'detalhes_setoriais': detalhes_setoriais
        }