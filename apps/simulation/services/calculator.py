from decimal import Decimal
import logging
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

class TaxCalculator:
    """
    Serviço central para cálculo de impostos (Cenário Atual vs. Cenário Reforma).
    Busca alíquotas do banco de dados com fallback para valores fixos.
    Utiliza camada de cache para otimização.
    """

    # Alíquotas para arredondamento (usadas na View)
    SN_AVERAGE_RATE = Decimal('0.01')
    REFORM_RATE = Decimal('0.01')

    # Alíquotas Fallback (caso o banco esteja vazio)
    FALLBACK_RATES = {
        'SIMPLES_NACIONAL': Decimal('0.1000'),
        'LUCRO_PRESUMIDO': Decimal('0.1633'), # PIS + COFINS + ISS + IRPJ + CSLL
        'REFORMA': Decimal('0.2650'),
    }

    @classmethod
    def get_rate(cls, rule_type):
        """
        Busca a alíquota ativa no banco de dados para o tipo de regime/reforma.
        Utiliza cache para evitar consultas excessivas.
        """
        cache_key = f"tax_rate_{rule_type}"
        cached_rate = cache.get(cache_key)
        
        if cached_rate is not None:
            return Decimal(str(cached_rate))

        from simulation.models import TaxRule # Import absoluto para evitar conflito de app_label
        
        try:
            rule = TaxRule.objects.filter(rule_type=rule_type, is_active=True).first()
            if rule:
                rate = rule.rate
                # Salva no cache
                cache.set(cache_key, float(rate), settings.CACHE_TTL)
                return rate
        except Exception as e:
            logger.error(f"Erro ao buscar alíquota {rule_type} no banco: {e}")
        
        return cls.FALLBACK_RATES.get(rule_type, Decimal('0.00'))

    @classmethod
    def calculate_current_tax(cls, company_data, financials):
        regime = company_data.get('tax_regime')
        revenue = financials.get('monthly_revenue')

        rate = cls.get_rate(regime)
        return revenue * rate

    @classmethod
    def calculate_reform_tax(cls, company_data, financials):
        revenue = financials.get('monthly_revenue')
        costs = financials.get('costs', Decimal('0.00'))
        
        # A reforma tributária (IBS/CBS) incide sobre o valor adicionado (Faturamento - Custos)
        value_added = max(Decimal('0.00'), revenue - costs)
        
        rate = cls.get_rate('REFORMA')
        return value_added * rate