from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from Expenses.models import Category, Transaction
from decimal import Decimal


@login_required(login_url='users:register')
def add_expense(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        category_obj = Category.objects.filter(id=category_id, user=request.user).first() if category_id else None
        
        Transaction.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            amount=Decimal(request.POST.get('amount')),
            transaction_type='expense', # Hardcoded type for explicit endpoint
            category=category_obj
        )
    return redirect('users:home')


@login_required(login_url='users:register')
def add_income(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        category_obj = Category.objects.filter(id=category_id, user=request.user).first() if category_id else None
        
        Transaction.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            amount=Decimal(request.POST.get('amount')),
            transaction_type='income', # Hardcoded type for explicit endpoint
            category=category_obj
        )
    return redirect('users:home')


@login_required(login_url='users:register')
def add_category(request):
    if request.method == 'POST':
        cat_name = request.POST.get('category_name').strip()
        if cat_name:
            Category.objects.get_or_create(user=request.user, name=cat_name)
    return redirect('users:home')

@login_required(login_url='users:register')
def delete_transaction(request, transaction_id):
    if request.method == 'POST':
        transaction = Transaction.objects.filter(id=transaction_id, user=request.user).first()
        if transaction:
            transaction.delete()
    return redirect('users:home')