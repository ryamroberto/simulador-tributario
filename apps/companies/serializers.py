from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'cnpj', 'monthly_revenue', 'sector', 
            'state', 'tax_regime', 'employees_count', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_monthly_revenue(self, value):
        if value <= 0:
            raise serializers.ValidationError("O faturamento mensal deve ser maior que zero.")
        return value
