from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import TaxRule, SuggestionMatrix

@receiver(post_save, sender=TaxRule)
@receiver(post_delete, sender=TaxRule)
def invalidate_tax_rule_cache(sender, instance, **kwargs):
    """
    Limpa o cache da alíquota quando uma TaxRule é salva ou deletada.
    """
    cache_key = f"tax_rate_{instance.rule_type}"
    cache.delete(cache_key)

@receiver(post_save, sender=SuggestionMatrix)
@receiver(post_delete, sender=SuggestionMatrix)
def invalidate_suggestion_cache(sender, instance, **kwargs):
    """
    Limpa o cache de sugestões quando uma SuggestionMatrix é salva ou deletada.
    """
    cache_key = f"suggestions_{instance.sector}_{instance.impact}"
    cache.delete(cache_key)
