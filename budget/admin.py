from django.contrib import admin

from budget.models import Budget, Category, CategoryItem


class CustomBudgetAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'income_monthly_total', 'expense_monthly_total', 'surplus_monthly')
    list_filter = ('created_by', )

class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'total_monthly', 'budget')
    list_filter = ('budget', 'c_type', )

class CustomCategoryItemAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'monthly', 'category', 'get_budget')
    list_filter = ('category', )

admin.site.register(Budget, CustomBudgetAdmin)
admin.site.register(Category, CustomCategoryAdmin)
admin.site.register(CategoryItem, CustomCategoryItemAdmin)