from django.contrib import admin
from django.urls import path
from Users import views as users_views
from Expenses import views as expenses_views

app_name = 'expenses' 

urlpatterns = [
    path('expense/add', expenses_views.add_expense, name = 'add_expense'),
    path('add_form', expenses_views.add_expense_from_form, name = 'add_expense_from_form'),
    path('add_expense_from_form_submission', expenses_views.add_expense_from_form_submission, name = 'add_expense_from_form_submission'),
    path('income/add', expenses_views.add_income, name = 'add_income'),
    path('category/add', expenses_views.add_category, name = 'add_category'),
    path('transaction/delete/<int:transaction_id>/', expenses_views.delete_transaction, name = 'delete_transaction'),
    path('transaction/edit/<int:transaction_id>/', expenses_views.edit_transaction, name = 'edit_transaction'),
    path('chart/piechart',expenses_views.piechart,name='piechart'),
    path("transactions/",expenses_views.transaction_history,name="transaction_history"),
]