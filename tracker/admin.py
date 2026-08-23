from django.contrib import admin
from .models import Category, Notification, Transaction,Budget,SavingsGoal

admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(SavingsGoal)
admin.site.register(Notification)