from django.contrib import admin
from django.urls import path
from Users import views as users_views
from Expenses import views as expenses_views

app_name = 'expenses' 

urlpatterns = [
    path('expense/add', expenses_views.add_expense, name = 'add_expense'),
    path('income/add', expenses_views.add_income, name = 'add_income'),
    path('category/add', expenses_views.add_category, name = 'add_category'),
    path('transaction/delete/<int:transaction_id>/', expenses_views.delete_transaction, name = 'delete_transaction'),
]