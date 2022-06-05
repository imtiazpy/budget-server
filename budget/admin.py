from django.contrib import admin

from budget.models import Budget, Category, CategoryItem


admin.site.register(Budget)
admin.site.register(Category)
admin.site.register(CategoryItem)