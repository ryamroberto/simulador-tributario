from rest_framework import serializers
from companies.models import Company
from .models import SimulationLog, TaxRule, SuggestionMatrix
from drf_spectacular.utils import extend_schema_field

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
        help_text="Faturamento bruto mensal da empresa.",
        initial=10000.00
    )
    costs = serializers.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        required=True,
        label="Custos Mensais",
        help_text="Custos operacionais mensais dedutíveis.",
        initial=2000.00
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

    class Meta:
        swagger_schema_fields = {
            "example": {
                "monthly_revenue": 50000.00,
                "costs": 15000.00,
                "tax_regime": "LUCRO_PRESUMIDO",
                "sector": "SERVICOS",
                "state": "SP"
            }
        }

    def validate_monthly_revenue(self, value):
        if value <= 0:
            raise serializers.ValidationError("O faturamento deve ser um valor positivo.")
        return value

    def validate_costs(self, value):
        if value < 0:
            raise serializers.ValidationError("Os custos não podem ser negativos.")
        return value

    def validate(self, data):
        revenue = data.get('monthly_revenue')
        costs = data.get('costs')
        if revenue and costs and costs > revenue:
            raise serializers.ValidationError({
                "costs": "Os custos operacionais não podem ser maiores que o faturamento mensal nesta simulação simplificada."
            })
        return data


class SimulationLogListSerializer(serializers.ModelSerializer):
    """
    Serializer para listagem amigável do histórico de simulações.
    """
    regime_tributario_desc = serializers.CharField(source='get_tax_regime_display', read_only=True)
    setor_desc = serializers.CharField(source='get_sector_display', read_only=True)
    impacto_desc = serializers.CharField(source='get_impact_classification_display', read_only=True)
    data_criacao = serializers.DateTimeField(source='created_at', format="%d/%m/%Y %H:%M", read_only=True)

    class Meta:
        model = SimulationLog
        fields = [
            'id',
            'company',
            'monthly_revenue',
            'costs',
            'tax_regime',
            'regime_tributario_desc',
            'sector',
            'setor_desc',
            'state',
            'current_tax_load',
            'reform_tax_load',
            'delta_value',
            'impact_classification',
            'impacto_desc',
            'data_criacao'
        ]
        read_only_fields = fields


class TaxRuleSerializer(serializers.ModelSerializer):
    """
    Serializer para gestão administrativa de regras tributárias.
    """
    class Meta:
        model = TaxRule
        fields = '__all__'


class SuggestionMatrixSerializer(serializers.ModelSerializer):
    """
    Serializer para gestão administrativa da matriz de sugestões.
    """
    class Meta:
        model = SuggestionMatrix
        fields = '__all__'
