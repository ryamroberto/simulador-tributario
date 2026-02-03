from rest_framework import serializers
from companies.models import Company

class SimulationInputSerializer(serializers.Serializer):
    """
    Valida os dados necessários para rodar uma simulação.
    """
    company_id = serializers.IntegerField(required=False, help_text="ID da empresa cadastrada (opcional)")
    
    # Se company_id não for fornecido, estes campos tornam-se obrigatórios para uma simulação "on-the-fly"
    monthly_revenue = serializers.DecimalField(max_digits=15, decimal_places=2, required=True)
    costs = serializers.DecimalField(max_digits=15, decimal_places=2, required=True)
    tax_regime = serializers.ChoiceField(choices=Company.TaxRegime.choices, required=True)
    sector = serializers.ChoiceField(choices=Company.Sector.choices, required=True)
    state = serializers.ChoiceField(choices=Company.UF.choices, required=False)

    def validate_monthly_revenue(self, value):
        if value <= 0:
            raise serializers.ValidationError("O faturamento deve ser maior que zero.")
        return value

    def validate_costs(self, value):
        if value < 0:
            raise serializers.ValidationError("Os custos não podem ser negativos.")
        return value
