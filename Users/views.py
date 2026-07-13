from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm 
from django.contrib.auth import login as  django_login, logout as django_logout
from decimal import Decimal
from datetime import date
from Expenses.models import Category, Transaction
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.db.models import Sum,Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='users:login')
def home(request):
    current_user = request.user
    today = date.today()

    # Fetch records for the current user and month
    user_txns_for_current_month = Transaction.objects.filter(
        user=current_user, 
        date__year=today.year, 
        date__month=today.month,
        # date = today
    ).aggregate(
        total_income = Sum('amount', filter = Q(transaction_type = 'income')),
        total_expenses = Sum('amount', filter = Q(transaction_type = 'expense'))
    )
    user_categories = Category.objects.filter(user=current_user)  

    print(f"user_txns_for_current_month------{user_txns_for_current_month}")

    # today_transactions = Transaction.objects.filter(user=current_user,date__date = today).order_by('-date')
    recent_transactions = Transaction.objects.filter(user=current_user).order_by('-date')[:5]

    context = {
        'transactions': recent_transactions,
        'categories': user_categories,
        'total_income': f"{(user_txns_for_current_month['total_income'] or 0):,.2f}",
        'total_expenses': f"{(user_txns_for_current_month['total_expenses'] or 0):,.2f}",
        'net_balance': f"{(user_txns_for_current_month['total_income'] or 0) - (user_txns_for_current_month['total_expenses'] or 0):,.2f}",
    }
    return render(request, 'home.html', context)

from django.contrib.auth.hashers import make_password

def register(request):
    try:
        if request.method == 'POST':
            # Create a new user object from POST data, but don't save yet!
            print(f"Request POST data: {request.POST}")  # Debugging line to check POST data
            form = CustomUserCreationForm(request.POST)
            
            if form.is_valid():
                # Create a new user instance but don't save to the database yet
                new_user = form.save(commit=False)
                
                # Set the username and email from the form data
                new_user.username = form.cleaned_data['UserName']
                new_user.email = form.cleaned_data['Email']
                
                # Hash the password before saving
                new_user.password = make_password(form.cleaned_data['password1'])
                
                # Save the user to the database
                new_user.save()
                
                # # Optionally, you can log the user in immediately after registration
                django_login(request, new_user, backend='Users.backends.EmailOrUsernameBackend')
                
                default_categories = [
                    Category(user = request.user,name = "Food"),
                    Category(user = request.user,name = "Transport"),
                    Category(user = request.user,name = "Groceries")
                ]

                DefaultCategories = Category.objects.bulk_create(default_categories)

                # Redirect to home or any other page after successful registration
                return redirect('users:home')
            # Save the user to the database (this should set the correct username and hashed password)
            form.save()
            
            # Now you can return a success message or redirect to another page...
        else:
            form = CustomUserCreationForm()  # Initialize an empty form if not POST
        return render(request, 'register.html', {'form': form})
    except Exception as e:
        # Handle the exception, e.g., log it or display an error message
        return render(request, 'register.html', {'form': form, 'error_message': str(e)})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            django_login(request,form.get_user())
            return redirect('users:home')
    else:
        form = AuthenticationForm()
    # 📌 THIS LINE IS REQUIRED: This updates the dynamic label rendering in your HTML
    form.fields['username'].label = "Username / Email"
    form.fields['username'].widget.attrs['placeholder'] = "Enter your username or email"
       

    return render(request, 'login.html', {"form":form})

def logout(request):
    if request.method == 'POST':
        django_logout(request)
        return redirect('users:login')
    return redirect('users:home')
