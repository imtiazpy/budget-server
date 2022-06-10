from django.contrib import admin

from budget.models import Budget, Category, CategoryItem


class CustomBudgetAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'income_monthly_total', 'expense_monthly_total', 'surplus_monthly')

class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'total_monthly', 'budget')

class CustomCategoryItemAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'monthly', 'category', 'get_budget')

admin.site.register(Budget, CustomBudgetAdmin)
admin.site.register(Category, CustomCategoryAdmin)
admin.site.register(CategoryItem, CustomCategoryItemAdmin)