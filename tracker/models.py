from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    CATEGORY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    class Meta:
        verbose_name_plural = "Categories"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.amount} on {self.date}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    limit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ("user", "category", "start_date", "end_date")

    def get_total_spent(self):
        total_spent = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            transaction_type='expense',
            date__range=(self.start_date, self.end_date)
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        return total_spent

    def percent_used(self):
        if self.limit_amount > 0:
            return Decimal(self.get_total_spent() / self.limit_amount) * 100
        return 0

    def is_over_budget(self):
        return self.get_total_spent() > self.limit_amount   

    def get_remaining_budget(self):
        return self.limit_amount - self.get_total_spent()   

    def get_budget_status(self):
        if self.is_over_budget():
            return "Over Budget"
        elif self.percent_used() > 80:
            return "Close to Budget Limit"
        else:
            return "Within Budget"

    def __str__(self):
        return f"{self.category.name} - {self.limit_amount} from {self.start_date} to {self.end_date}"

class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    target_date = models.DateField()

    def progress_percentage(self):
        if self.target_amount > 0:
            return (Decimal(self.current_amount / self.target_amount)) * 100
        return Decimal('0')

    def __str__(self):
        return f"{self.name} - {self.current_amount}/{self.target_amount}" 