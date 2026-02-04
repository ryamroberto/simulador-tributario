from django.contrib import admin
from .models import TaxRule, SuggestionMatrix

@admin.register(TaxRule)
class TaxRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'rule_type', 'sector', 'state', 'rate', 'is_active')
    list_filter = ('rule_type', 'sector', 'state', 'is_active')
    search_fields = ('name',)

@admin.register(SuggestionMatrix)
class SuggestionMatrixAdmin(admin.ModelAdmin):
    list_display = ('sector', 'impact', 'short_suggestion')
    list_filter = ('sector', 'impact')
    search_fields = ('suggestion_text',)

    def short_suggestion(self, obj):
        return obj.suggestion_text[:100] + "..." if len(obj.suggestion_text) > 100 else obj.suggestion_text
    short_suggestion.short_description = "Sugestão"