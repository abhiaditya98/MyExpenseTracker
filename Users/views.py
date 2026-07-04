from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm 
from django.contrib.auth import login as  django_login, logout as django_logout
from decimal import Decimal
from datetime import date
from Expenses.models import Category, Transaction
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
# Create your views here.
@login_required(login_url='users:login')
def home(request):
    current_user = request.user
    today = date.today()

    # Fetch records for the current user and month
    user_txns = Transaction.objects.filter(
        user=current_user, 
        date__year=today.year, 
        date__month=today.month
    )
    user_categories = Category.objects.filter(user=current_user)

    # Perform calculations
    total_income = user_txns.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_expenses = user_txns.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    net_balance = total_income - total_expenses

    context = {
        'transactions': user_txns,
        'categories': user_categories,
        'total_income': f"{total_income:,.2f}",
        'total_expenses': f"{total_expenses:,.2f}",
        'net_balance': f"{net_balance:,.2f}",
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html',{"form":form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            django_login(request,form.get_user())
            return redirect('users:home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {"form":form})

def logout(request):
    if request.method == 'POST':
        django_logout(request)
        return redirect('users:login')
    return redirect('users:home')

# @login_required
# def home(request):
#     current_user = request.user
#     today = date.today()

#     # Fetch records for the current user and month
#     user_txns = Transaction.objects.filter(
#         user=current_user, 
#         date__year=today.year, 
#         date__month=today.month
#     )
#     user_categories = Category.objects.filter(user=current_user)

#     # Perform calculations
#     total_income = user_txns.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
#     total_expenses = user_txns.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
#     net_balance = total_income - total_expenses

#     context = {
#         'transactions': user_txns,
#         'categories': user_categories,
#         'total_income': f"{total_income:,.2f}",
#         'total_expenses': f"{total_expenses:,.2f}",
#         'net_balance': f"{net_balance:,.2f}",
#     }
#     return render(request, 'home.html', context)   