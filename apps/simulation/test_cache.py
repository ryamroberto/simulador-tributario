from django.test import TestCase
from django.core.cache import cache
from decimal import Decimal
from .models import TaxRule, SuggestionMatrix
from .services.calculator import TaxCalculator
from .services.analyzer import ImpactAnalyzer

class CacheSystemTest(TestCase):
    def setUp(self):
        cache.clear()
        # Limpa dados de migrações para evitar conflitos
        TaxRule.objects.all().delete()
        SuggestionMatrix.objects.all().delete()
        
        # Cria dados iniciais
        self.rule = TaxRule.objects.create(
            name="Teste SN",
            rule_type='SIMPLES_NACIONAL',
            rate=Decimal('0.1500')
        )
        self.suggestion = SuggestionMatrix.objects.create(
            sector='SERVICOS',
            impact='POSITIVO',
            suggestion_text="Sugestão Original"
        )

    def test_tax_rate_caching(self):
        # Primeira chamada: popula o cache
        rate = TaxCalculator.get_rate('SIMPLES_NACIONAL')
        self.assertEqual(rate, Decimal('0.1500'))
        
        # Verifica se está no cache
        self.assertIsNotNone(cache.get('tax_rate_SIMPLES_NACIONAL'))

        # Altera no banco sem usar o ORM save (direto via update) para não disparar o signal
        TaxRule.objects.filter(id=self.rule.id).update(rate=Decimal('0.2000'))
        
        # A chamada ainda deve retornar o valor antigo do cache
        rate_cached = TaxCalculator.get_rate('SIMPLES_NACIONAL')
        self.assertEqual(rate_cached, Decimal('0.1500'))

    def test_tax_rate_invalidation(self):
        # Popula cache
        TaxCalculator.get_rate('SIMPLES_NACIONAL')
        
        # Altera via ORM save (dispara signal)
        self.rule.rate = Decimal('0.2500')
        self.rule.save()
        
        # O cache deve estar limpo
        self.assertIsNone(cache.get('tax_rate_SIMPLES_NACIONAL'))
        
        # Nova chamada deve trazer o valor novo
        rate_new = TaxCalculator.get_rate('SIMPLES_NACIONAL')
        self.assertEqual(rate_new, Decimal('0.2500'))

    def test_suggestion_caching_and_invalidation(self):
        # Primeira chamada: popula cache
        suggestions = ImpactAnalyzer.get_suggestions('SERVICOS', 'POSITIVO')
        self.assertIn("Sugestão Original", suggestions)
        
        # Altera via save (dispara signal)
        self.suggestion.suggestion_text = "Sugestão Nova"
        self.suggestion.save()
        
        # Cache deve estar vazio
        self.assertIsNone(cache.get('suggestions_SERVICOS_POSITIVO'))
        
        # Nova chamada traz dado novo
        suggestions_new = ImpactAnalyzer.get_suggestions('SERVICOS', 'POSITIVO')
        self.assertIn("Sugestão Nova", suggestions_new)
