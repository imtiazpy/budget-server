from rest_framework import serializers
from budget.models import Budget, CategoryItem, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class BudgetListSerializer(serializers.ModelSerializer):
    """Serializer for the list view of the Budget Model"""
    class Meta:
        model = Budget
        fields = ('id', 'name', )



class CategoryItemSerializer(serializers.ModelSerializer):
    """For Listing and creating"""
    class Meta:
        model = CategoryItem
        fields = '__all__'
    
    def validate_category(self, value):
        """
        This function checks if the user is the owner of Category, before allowing the user to push a CategoryItem to the Category
        """
        category = Category.objects.get(id=value.id)
        user = self.context['request'].user

        if category.budget.created_by != user:
            raise serializers.ValidationError("You do not have permission to perform this action")
        return value


class CategorySerializer(serializers.ModelSerializer):

    items = CategoryItemSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'
    
    def validate_budget(self, value):
        """
        This function checks if the user is the owner of the Budget, before allowing the user to push a Category into the Budget.
        """
        budget = Budget.objects.get(id=value.id)
        user = self.context['request'].user
        
        if budget.created_by != user:
            raise serializers.ValidationError("You do not have permission to perform this action")
        
        return value


class BudgetSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, source='custom_categories')
    income = CategorySerializer(read_only=True)
    expense = CategorySerializer(read_only=True)
    class Meta:
        model = Budget
        fields = '__all__'