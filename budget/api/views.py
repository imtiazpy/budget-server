from rest_framework import generics
from django.shortcuts import get_object_or_404
from budget.models import Budget
from budget.api.serializers import BudgetListSerializer, BudgetDetailSerializer


class BudgetListView(generics.ListAPIView):
    """
    View for listing all the Budget of the authorized user
    Initial Budget will be created upon user registration
    All the Budgets after the initial one will be created with copy action
    """
    serializer_class = BudgetListSerializer

    def get_queryset(self):
        return Budget.objects.filter(created_by=self.request.user).order_by('order')


class BudgetDetailView(generics.RetrieveAPIView):
    """View for showing detailed data of selected Budget"""
    serializer_class = BudgetDetailSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Budget.objects.filter(created_by=self.request.user)