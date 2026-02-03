from rest_framework import serializers
from companies.models import Company

class SimulationInputSerializer(serializers.Serializer):
    """
    Valida os dados necessários para rodar uma simulação.
    """
    company_id = serializers.IntegerField(
        required=False, 
        label="ID da Empresa",
        help_text="ID da empresa cadastrada no sistema (opcional)."
    )
    
    monthly_revenue = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        required=True,
        label="Faturamento Mensal",
        help_text="Faturamento bruto mensal da empresa."
    )
    costs = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        required=True,
        label="Custos Mensais",
        help_text="Custos operacionais mensais dedutíveis."
    )
    tax_regime = serializers.ChoiceField(
        choices=Company.TaxRegime.choices, 
        required=True,
        label="Regime Tributário",
        help_text="Regime tributário atual da empresa (Simples Nacional ou Lucro Presumido)."
    )
    sector = serializers.ChoiceField(
        choices=Company.Sector.choices, 
        required=True,
        label="Setor de Atuação",
        help_text="Setor econômico da empresa."
    )
    state = serializers.ChoiceField(
        choices=Company.UF.choices, 
        required=False,
        label="UF",
        help_text="Unidade Federativa onde a empresa está sediada."
    )

    def validate_monthly_revenue(self, value):
        if value <= 0:
            raise serializers.ValidationError("O faturamento deve ser maior que zero.")
        return value

    def validate_costs(self, value):
        if value < 0:
            raise serializers.ValidationError("Os custos não podem ser negativos.")
        return value