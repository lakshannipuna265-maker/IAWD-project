from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Category,Transaction
from .forms import CategoryForm, TransactionForm     

def dashboard(request):
    return render(request, 'tracker/dashboard.html')

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
            transaction.save()
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
            form.save()
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