from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Category, Notification, SavingsGoal,Transaction, Budget
from .forms import BudgetForm, CategoryForm, SavingsGoalForm, TransactionForm     
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required
def dashboard(request):
    context = {
        'transaction_count': Transaction.objects.filter(user=request.user).count(),
        'budgets': Budget.objects.filter(user=request.user),
        'goals': SavingsGoal.objects.filter(user=request.user),
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def category_list(request): 
    categories = Category.objects.filter(user=request.user)
    return render(request, 'tracker/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'tracker/category_form.html', {'form': form})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'tracker/category_form.html', {'form': form})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'tracker/category_confirm_delete.html', {'category': category})

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/transaction_list.html', {'transactions': transactions})

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.transaction_type = transaction.category.category_type         
            transaction.save()
            check_budget_notifications(transaction)
            return redirect('transaction_list')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'tracker/transaction_form.html', {'form': form})

@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.transaction_type = transaction.category.category_type 
            transaction.save()
            check_budget_notifications(transaction)
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    return render(request, 'tracker/transaction_form.html', {'form': form})

@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'tracker/transaction_confirm_delete.html', {'transaction': transaction})

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'tracker/budget_list.html', {'budgets': budgets})

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            try:
                budget.save()
                return redirect('budget_list')
            except IntegrityError: 
                form.add_error(None, "category already has a budget for the selected date range.")
    else:
        form = BudgetForm(user=request.user)
    return render(request, 'tracker/budget_form.html', {'form': form})

@login_required
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget, user=request.user)
        if form.is_valid():
            try:
                form.save()
                return redirect('budget_list')
            except IntegrityError:
                form.add_error(None, "category already has a budget for the selected date range.")
    else:
        form = BudgetForm(instance=budget, user=request.user)
    return render(request, 'tracker/budget_form.html', {'form': form})

@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget_list')
    return render(request, 'tracker/budget_confirm_delete.html', {'budget': budget})

@login_required
def savingsgoal_list(request):
    goals = SavingsGoal.objects.filter(user=request.user)
    return render(request, 'tracker/savingsgoal_list.html', {'goals': goals})

@login_required
def savingsgoal_create(request):
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('savingsgoal_list')
    else:
        form = SavingsGoalForm()
    return render(request, 'tracker/savingsgoal_form.html', {'form': form})

@login_required
def savingsgoal_update(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('savingsgoal_list')
    else:
        form = SavingsGoalForm(instance=goal)
    return render(request, 'tracker/savingsgoal_form.html', {'form': form})

@login_required
def savingsgoal_delete(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        return redirect('savingsgoal_list')
    return render(request, 'tracker/savingsgoal_confirm_delete.html', {'goal': goal})

@login_required
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def check_budget_notifications(transaction):
    affected_budgets = Budget.objects.filter(
        user=transaction.user,
        category=transaction.category,
        start_date__lte=transaction.date,
        end_date__gte=transaction.date
    )
    for budget in affected_budgets:
        percent = budget.percent_used()
        if percent >= 100 and not budget.notified_100:
            Notification.objects.create(
                user=budget.user,
                budget=budget,
                message=f"Your {budget.category.name} budget is over 100%! Spent {budget.get_total_spent()} / {budget.limit_amount}."
            )
            budget.notified_100 = True
            budget.save()
        elif percent >= 80 and not budget.notified_80:
            Notification.objects.create(
                user=budget.user,
                budget=budget,
                message=f"Your {budget.category.name} budget has reached 80% ({budget.get_total_spent()} / {budget.limit_amount})."
            )
            budget.notified_80 = True
            budget.save()

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'tracker/notification_list.html', {'notifications': notifications})

@login_required
def notification_mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')