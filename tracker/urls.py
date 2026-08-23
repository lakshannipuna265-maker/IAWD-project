from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.transaction_create, name='transaction_create'),
    path('transactions/<int:pk>/edit/', views.transaction_update, name='transaction_update'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.budget_create, name='budget_create'),
    path('budgets/<int:pk>/edit/', views.budget_update, name='budget_update'),
    path('budgets/<int:pk>/delete/', views.budget_delete, name='budget_delete'),
    path('savingsgoals/', views.savingsgoal_list, name='savingsgoal_list'),
    path('savingsgoals/add/', views.savingsgoal_create, name='savingsgoal_create'),
    path('savingsgoals/<int:pk>/edit/', views.savingsgoal_update, name='savingsgoal_update'),
    path('savingsgoals/<int:pk>/delete/', views.savingsgoal_delete, name='savingsgoal_delete'),
    path('register/', views.register, name='register'),    
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:pk>/read/', views.notification_mark_read, name='notification_mark_read'),  
]