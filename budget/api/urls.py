from django.urls import path
from budget.api.views import BudgetListView, BudgetDetailView

urlpatterns = [
    path('budgets/', BudgetListView.as_view(), name='budgets'),
    path('budget/<int:id>/', BudgetDetailView.as_view(), name='budget-detail'),
]