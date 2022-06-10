from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import Http404
from budget.models import Budget, CategoryItem, Category
from budget.api.serializers import (
    BudgetListSerializer, BudgetSerializer, CategorySerializer, CategoryItemSerializer
)


class BudgetListCreateView(generics.ListCreateAPIView):
    """
    View for Creating and  Listing all the Budget of the authorized user.
    One Budget will be created upon user registration initially.
    """

    def get_queryset(self):
        return Budget.objects.filter(created_by=self.request.user).order_by('order')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BudgetSerializer
        return BudgetListSerializer

    def perform_create(self, serializer):
        data = serializer.data
        budget = Budget(name=data['name'], created_by=self.request.user)
        budget.save()
        income = Category(name='Income', budget=budget, c_type=1, persistent=True)
        income.save()

        expense = Category(name='Expense', budget=budget, c_type=2, persistent=True)
        expense.save()

        budget.income = income
        budget.expense = expense
        budget.save()


class BudgetRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """View for showing detailed data of selected Budget"""
    serializer_class = BudgetSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Budget.objects.filter(created_by=self.request.user)


class CategoryListCreateView(generics.ListCreateAPIView):
    """For Creating and listing the Category Tables"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(budget__created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save()


class CategoryUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """View for Retrieve Update and Delete"""
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get_queryset(self):
        """querying category that are listed in budget created by the current user"""
        return Category.objects.filter(budget__created_by=self.request.user)


class CategoryItemListCreateView(generics.ListCreateAPIView):
    """View for Creating and Listing CategoryItem"""
    serializer_class = CategoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CategoryItem.objects.filter(category__budget__created_by=self.request.user).order_by('order')
    
    def perform_create(self, serializer):
        serializer.save()
    
    
    # TODO: add move_up and move_down method


class CategoryItemUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """For Updating and Deleting the Item"""
    serializer_class = CategoryItemSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return CategoryItem.objects.filter(category__budget__created_by=self.request.user)






