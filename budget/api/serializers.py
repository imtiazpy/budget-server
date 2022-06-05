from rest_framework import serializers
from budget.models import Budget

class BudgetListSerializer(serializers.ModelSerializer):
    """Serializer for the list view of the Budget Model"""
    class Meta:
        model = Budget
        fields = ('id', 'name', )


class BudgetDetailSerializer(serializers.ModelSerializer):
    """Serializer for the detail view of the Budget Model"""
    class Meta:
        model = Budget
        fields = '__all__'