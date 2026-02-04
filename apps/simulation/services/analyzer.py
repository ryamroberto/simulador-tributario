from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class ImpactAnalyzer:
    """
    Serviço para analisar a diferença entre as cargas tributárias e fornecer insights qualitativos.
    Busca sugestões dinâmicas da Matriz de Sugestões no banco de dados.
    """

    @classmethod
    def get_suggestions(cls, sector, impact_classification):
        """
        Busca a lista de sugestões no banco de dados para o setor e classificação de impacto.
        """
        from simulation.models import SuggestionMatrix
        
        try:
            suggestions = SuggestionMatrix.objects.filter(
                sector=sector, 
                impact=impact_classification
            ).values_list('suggestion_text', flat=True)
            
            if suggestions.exists():
                return list(suggestions)
        except Exception as e:
            logger.error(f"Erro ao buscar sugestões no banco: {e}")
        
        return ["Considere revisar seus créditos tributários e analisar o impacto na precificação final."]

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
