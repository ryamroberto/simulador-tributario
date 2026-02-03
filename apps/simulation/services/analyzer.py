from decimal import Decimal

class ImpactAnalyzer:
    """
    Serviço para analisar a diferença entre as cargas tributárias.
    """

    @classmethod
    def analyze(cls, current_tax, reform_tax):
        delta_value = reform_tax - current_tax
        
        if current_tax > 0:
            delta_percentage = (delta_value / current_tax) * 100
        else:
            delta_percentage = Decimal('0.00')

        if delta_value > 0:
            classification = 'NEGATIVO'
            message = "Sua carga tributária deve aumentar com a reforma."
        elif delta_value < 0:
            classification = 'POSITIVO'
            message = "Sua carga tributária deve diminuir com a reforma."
        else:
            classification = 'NEUTRO'
            message = "Sua carga tributária deve permanecer estável."

        return {
            'delta_value': delta_value,
            'delta_percentage': delta_percentage.quantize(Decimal('0.01')),
            'impact_classification': classification,
            'message': message
        }
