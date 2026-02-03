from decimal import Decimal

class TaxCalculator:
    """
    Serviço central para cálculo de impostos (Cenário Atual vs. Cenário Reforma).
    Regras fixas conforme especificado no PRD.
    """

    # Alíquotas Lucro Presumido (Simplificadas)
    LP_PIS = Decimal('0.0065')
    LP_COFINS = Decimal('0.03')
    LP_ISS = Decimal('0.05')
    LP_IRPJ = Decimal('0.048')  # Simplificado: 32% base * 15% alíquota
    LP_CSLL = Decimal('0.0288') # Simplificado: 32% base * 9% alíquota

    # Alíquota Simples Nacional (Média fixa simplificada)
    SN_AVERAGE_RATE = Decimal('0.10')

    # Alíquota Reforma (IBS + CBS estimada)
    REFORM_RATE = Decimal('0.265')

    @classmethod
    def calculate_current_tax(cls, company_data, financials):
        regime = company_data.get('tax_regime')
        revenue = financials.get('monthly_revenue')

        if regime == 'SIMPLES_NACIONAL':
            return revenue * cls.SN_AVERAGE_RATE
        
        if regime == 'LUCRO_PRESUMIDO':
            # Soma das alíquotas fixas para o Lucro Presumido
            total_rate = cls.LP_PIS + cls.LP_COFINS + cls.LP_ISS + cls.LP_IRPJ + cls.LP_CSLL
            return revenue * total_rate
        
        return Decimal('0.00')

    @classmethod
    def calculate_reform_tax(cls, company_data, financials):
        revenue = financials.get('monthly_revenue')
        costs = financials.get('costs', Decimal('0.00'))
        
        # A reforma tributária (IBS/CBS) incide sobre o valor adicionado (Faturamento - Custos)
        # Em um sistema de IVA não-cumulativo pleno.
        value_added = max(Decimal('0.00'), revenue - costs)
        
        # Nota: IRPJ e CSLL continuam existindo, mas para este simulador simplificado
        # focamos no impacto do IBS/CBS vs impostos sobre consumo atuais.
        # No entanto, para manter a comparabilidade com o Lucro Presumido (que inclui IRPJ/CSLL no cálculo acima),
        # assumiremos que IRPJ/CSLL permanecem constantes ou o foco é apenas no delta de consumo.
        # Decisão: Manter o foco no delta de carga total estimada.
        
        return value_added * cls.REFORM_RATE
