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