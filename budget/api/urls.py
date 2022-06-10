from django.urls import path
from budget.api.views import (
    BudgetListCreateView, BudgetRetrieveUpdateDeleteView, CategoryListCreateView, CategoryUpdateDeleteView, CategoryItemListCreateView, CategoryItemUpdateDeleteView,
)

urlpatterns = [
    path('budgets/', BudgetListCreateView.as_view(), name='budgets'),
    path('budget/<int:id>/', BudgetRetrieveUpdateDeleteView.as_view(), name='budget'),
    path('items/', CategoryItemListCreateView.as_view(), name='items'),
    path('item/<int:id>/', CategoryItemUpdateDeleteView.as_view(), name='item'),
    path('categories/', CategoryListCreateView.as_view(), name='categories'),
    path('category/<int:id>/', CategoryUpdateDeleteView.as_view(), name='category'),
]