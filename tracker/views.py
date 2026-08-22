from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category
from .forms import CategoryForm     

def dashboard(request):
    return render(request, 'tracker/dashboard.html')

@login_required
def category_list(request): 
    categories = Category.objects.filter(user=request.user)
    return render(request, 'tracker/category_list.html', {'categories': categories})
