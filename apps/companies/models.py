from django.db import models
from core.models import TimeStampedModel
from core.validators import validate_cnpj

class Company(TimeStampedModel):
    class Sector(models.TextChoices):
        SERVICES = 'SERVICOS', 'Serviços'
        COMMERCE = 'COMERCIO', 'Comércio'
        INDUSTRY = 'INDUSTRIA', 'Indústria'

    class TaxRegime(models.TextChoices):
        SIMPLES_NACIONAL = 'SIMPLES_NACIONAL', 'Simples Nacional'
        LUCRO_PRESUMIDO = 'LUCRO_PRESUMIDO', 'Lucro Presumido'

    class UF(models.TextChoices):
        AC = 'AC', 'Acre'
        AL = 'AL', 'Alagoas'
        AP = 'AP', 'Amapá'
        AM = 'AM', 'Amazonas'
        BA = 'BA', 'Bahia'
        CE = 'CE', 'Ceará'
        DF = 'DF', 'Distrito Federal'
        ES = 'ES', 'Espírito Santo'
        GO = 'GO', 'Goiás'
        MA = 'MA', 'Maranhão'
        MT = 'MT', 'Mato Grosso'
        MS = 'MS', 'Mato Grosso do Sul'
        MG = 'MG', 'Minas Gerais'
        PA = 'PA', 'Pará'
        PB = 'PB', 'Paraíba'
        PR = 'PR', 'Paraná'
        PE = 'PE', 'Pernambuco'
        PI = 'PI', 'Piauí'
        RJ = 'RJ', 'Rio de Janeiro'
        RN = 'RN', 'Rio Grande do Norte'
        RS = 'RS', 'Rio Grande do Sul'
        RO = 'RO', 'Rondônia'
        RR = 'RR', 'Roraima'
        SC = 'SC', 'Santa Catarina'
        SP = 'SP', 'São Paulo'
        SE = 'SE', 'Sergipe'
        TO = 'TO', 'Tocantins'

    name = models.CharField(max_length=255, verbose_name="Nome da Empresa")
    cnpj = models.CharField(
        max_length=18, 
        unique=True, 
        validators=[validate_cnpj], 
        verbose_name="CNPJ",
        help_text="Formato: 00.000.000/0000-00 ou apenas números."
    )
    monthly_revenue = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Faturamento Mensal")
    sector = models.CharField(max_length=20, choices=Sector.choices, verbose_name="Setor de Atuação")
    state = models.CharField(max_length=2, choices=UF.choices, verbose_name="UF")
    tax_regime = models.CharField(max_length=20, choices=TaxRegime.choices, verbose_name="Regime Tributário Atual")
    employees_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Número de Funcionários")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"