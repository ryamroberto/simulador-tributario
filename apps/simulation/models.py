from django.db import models
from core.models import TimeStampedModel
from companies.models import Company

class TaxRule(TimeStampedModel):
    class RuleType(models.TextChoices):
        SIMPLES_NACIONAL = 'SIMPLES_NACIONAL', 'Simples Nacional'
        LUCRO_PRESUMIDO = 'LUCRO_PRESUMIDO', 'Lucro Presumido'
        REFORMA = 'REFORMA', 'Pós-Reforma (IBS/CBS)'

    name = models.CharField(max_length=100, verbose_name="Nome da Regra")
    rule_type = models.CharField(max_length=20, choices=RuleType.choices, verbose_name="Tipo de Regime/Regra")
    sector = models.CharField(
        max_length=20, 
        choices=Company.Sector.choices, 
        null=True, 
        blank=True, 
        verbose_name="Setor de Atuação"
    )
    state = models.CharField(
        max_length=2, 
        choices=Company.UF.choices, 
        null=True, 
        blank=True, 
        verbose_name="UF"
    )
    rate = models.DecimalField(max_digits=6, decimal_places=4, verbose_name="Alíquota (Ex: 0.1500)")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    def __str__(self):
        return f"{self.get_rule_type_display()} - {self.name} ({self.rate * 100}%)"

    class Meta:
        app_label = 'simulation'
        verbose_name = "Regra Tributária"
        verbose_name_plural = "Regras Tributárias"


class SuggestionMatrix(TimeStampedModel):
    class ImpactClassification(models.TextChoices):
        POSITIVE = 'POSITIVO', 'Positivo'
        NEUTRAL = 'NEUTRO', 'Neutro'
        NEGATIVE = 'NEGATIVO', 'Negativo'

    sector = models.CharField(max_length=20, choices=Company.Sector.choices, verbose_name="Setor")
    impact = models.CharField(
        max_length=10, 
        choices=ImpactClassification.choices, 
        verbose_name="Classificação de Impacto"
    )
    suggestion_text = models.TextField(verbose_name="Texto da Sugestão")

    def __str__(self):
        return f"{self.get_sector_display()} - {self.get_impact_display()}"

    class Meta:
        app_label = 'simulation'
        verbose_name = "Matriz de Sugestão"
        verbose_name_plural = "Matrizes de Sugestões"


class SimulationLog(TimeStampedModel):
    # Relacionamento Opcional
    company = models.ForeignKey(
        Company, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Empresa"
    )

    # Inputs
    monthly_revenue = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Faturamento Mensal")
    costs = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Custos")
    tax_regime = models.CharField(max_length=20, choices=Company.TaxRegime.choices, verbose_name="Regime Tributário")
    sector = models.CharField(max_length=20, choices=Company.Sector.choices, verbose_name="Setor de Atuação")
    state = models.CharField(max_length=2, choices=Company.UF.choices, null=True, blank=True, verbose_name="UF")

    # Resultados
    current_tax_load = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Carga Atual")
    reform_tax_load = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Carga Reforma")
    delta_value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Diferença Absoluta")
    impact_classification = models.CharField(
        max_length=10, 
        choices=SuggestionMatrix.ImpactClassification.choices, 
        verbose_name="Classificação de Impacto"
    )

    def __str__(self):
        return f"Simulação {self.id} - {self.get_tax_regime_display()} ({self.created_at.strftime('%d/%m/%Y %H:%M')})"

    class Meta:
        app_label = 'simulation'
        verbose_name = "Log de Simulação"
        verbose_name_plural = "Logs de Simulações"
        ordering = ['-created_at']