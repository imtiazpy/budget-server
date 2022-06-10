from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from datetime import date
from ordered_model.models import OrderedModel

User = get_user_model()

CATEGORY_TYPES = (
    (1, 'INCOME'),
    (2, 'EXPENSE'),
    (3, 'OTHERS'),
)

class Category(models.Model):
    """
    Model for Category 
    Each Table (Income , Expense) is a Category
    """
    budget = models.ForeignKey('budget.Budget', related_name='categories', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(_("Name"), max_length=150, null=True, blank=True)
    c_type = models.IntegerField(_("Type"), choices=CATEGORY_TYPES, default=3)
    persistent = models.BooleanField(_("Persistent"), default=False)
    order = models.IntegerField(_("Order"), default=0)
    total_weekly = models.DecimalField(_("Total Weekly"), default=0, max_digits=13, decimal_places=2)
    total_bi_weekly = models.DecimalField(_("Total Bi-Weekly"), default=0, max_digits=13, decimal_places=2)
    total_monthly = models.DecimalField(_("Total Monthly"), default=0, max_digits=13, decimal_places=2)
    total_yearly = models.DecimalField(_("Total Yearly"), default=0, max_digits=13, decimal_places=2)

    def __str__(self):
        return f'Category-{self.id}-{self.name}'

    @staticmethod
    def update_category_order(category, is_add=True):
        categories = Category.objects.filter(budget=category.budget, order__gte=category.order).exclude(id=category.id)

        for c in categories:
            if is_add:
                c.order += 1
            else:
                c.order -+ 1
            c.save()
    

class CategoryItem(OrderedModel):
    """
    Model for each item in the Category table
    """
    category = models.ForeignKey('budget.Category', related_name='items', on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=150)
    weekly= models.DecimalField(_("Weekly Net"), default=0, max_digits=13, decimal_places=2)
    bi_weekly= models.DecimalField(_("Bi-Weekly Net"), default=0, max_digits=13, decimal_places=2)
    monthly= models.DecimalField(_("Monthly Net"), default=0, max_digits=13, decimal_places=2)
    yearly= models.DecimalField(_("Yearly Net"), default=0, max_digits=13, decimal_places=2)
    ref_category = models.BigIntegerField(_("Ref Category"), null=True, blank=True)
    order_with_respect_to = 'category'

    def __str__(self):
        return f'CategoryItem-{self.id}-{self.name}'

    class Meta(OrderedModel.Meta):
        ordering = ['order', 'pk']



class Budget(models.Model):
    """Model for Main Budget"""
    name = models.CharField(_("Name"), max_length=150, null=True, blank=True)
    title = models.CharField(_("Title"), max_length=150, default="Summary of Monthly Budgeted Expenses", blank=True)
    pie_title = models.CharField(_("Pie Title"), max_length=150, null=True, blank=True)
    persistent = models.BooleanField(_("Persistent"), default=False)
    income = models.ForeignKey('budget.Category', related_name="income_budgets", on_delete=models.SET_NULL, null=True, blank=True)
    expense = models.ForeignKey('budget.Category', related_name="expense_budgets", on_delete=models.SET_NULL, null=True, blank=True)
    surplus_weekly = models.DecimalField(_("Surplus Weekly"), default=0, max_digits=13, decimal_places=2)
    surplus_bi_weekly = models.DecimalField(_("Surplus BeWeekly"), default=0, max_digits=13, decimal_places=2)
    surplus_monthly = models.DecimalField(_("Surplus Monthly"), default=0, max_digits=13, decimal_places=2)
    surplus_yearly = models.DecimalField(_("Surplus Yearly"), default=0, max_digits=13, decimal_places=2)
    created_by = models.ForeignKey(User, related_name="budgets", on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField(_("Order"), default=0)

    def __str__(self):
        return f"Budget-{self.id}-{self.name}"
    
    def custom_categories(self):
        # we have foreign key relation with Category model, related_name as categories
        return self.categories.filter(c_type=3).order_by('order')

    @staticmethod
    def init_budget(user):
        """
        This method will run while registering an account from the CustomUser Model.
        This method will create an initial instance of Budget along with Category for both Income and Expense for the registered user.
        """
        budget_name = f'Budget {date.today().year}'
        budget = Budget(name=budget_name, persistent=True, created_by=user)
        budget.save()

        income = Category(name='Income', budget=budget, c_type=1, persistent=True)
        income.save()

        expense = Category(name='Expense', budget=budget, c_type=2, persistent=True)
        expense.save()

        budget.income = income
        budget.expense = expense
        budget.save()

        return budget

    
    @staticmethod
    def update_budget_order(obj):
        budgets = Budget.objects.filter(created_by=obj.created_by, order__gt=obj.order)
        for b in budgets:
            b.order += 1
            b.save()
        obj.order += 1
        obj.save()


def update_category(instance):
    """
    updating the total field of Category Table while adding/deleting CategoryItem
    """
    _category = instance.category

    summary = _category.items.aggregate(Sum('weekly'), Sum('bi_weekly'), Sum('monthly'), Sum('yearly'))

    _category.total_weekly = summary['weekly__sum'] or 0
    _category.total_bi_weekly = summary['bi_weekly__sum'] or 0
    _category.total_monthly = summary['monthly__sum'] or 0
    _category.total_yearly = summary['yearly__sum'] or 0

    _category.save()

def on_update_item(sender, instance, created, *args, **kwargs):
    update_category(instance)

def on_delete_item(sender, instance, created, *args, **kwargs):
    update_category(instance)


def update_budget(sender, instance, created, *args, **kwargs):
    """
    Method used for updating the surplus fields of Budget while populating the Category table
    """
    _budget= instance.budget
    surplus_weekly = 0
    surplus_bi_weekly = 0
    surplus_monthly = 0
    surplus_yearly = 0

    if _budget.income:
        surplus_weekly += _budget.income.total_weekly    
        surplus_bi_weekly += _budget.income.total_bi_weekly    
        surplus_monthly += _budget.income.total_monthly    
        surplus_yearly += _budget.income.total_yearly    
    
    if _budget.expense:
        surplus_weekly -= _budget.expense.total_weekly    
        surplus_bi_weekly -= _budget.expense.total_bi_weekly    
        surplus_monthly -= _budget.expense.total_monthly    
        surplus_yearly -= _budget.expense.total_yearly
    
    _budget.surplus_weekly = surplus_weekly
    _budget.surplus_bi_weekly = surplus_bi_weekly
    _budget.surplus_monthly = surplus_monthly
    _budget.surplus_yearly = surplus_yearly

    _budget.save()

    # update ref item
    if _budget.expense:
        for item in _budget.expense.items.all():
            if item.ref_category == instance.id:
                item.name = instance.name
                item.save()
                break
        if created:
            Category.update_category_order(instance)


def on_delete_category(sender, instance, *args, **kwargs):
    """Method for deleting the Category Table"""
    _budget = instance.budget
    if _budget.expense:
        for item in _budget.expense.items.all():
            if item.ref_category == instance.id:
                item.delete()
                break
    Category.update_category_order(instance, False)

def set_budget_order(sender, instance, created, *args, **kwargs):
    if created:
        Budget.update_budget_order(instance)


post_save.connect(on_update_item, sender=CategoryItem)
# post_delete.connect(on_delete_item, sender=CategoryItem)

post_save.connect(update_budget, sender=Category)
# post_delete.connect(on_delete_category, sender=Category)

post_save.connect(set_budget_order, sender=Budget)