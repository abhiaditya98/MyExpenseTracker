from urllib import request

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from Expenses.models import Category, Transaction
from decimal import Decimal
from datetime import date
from django.db.models import Sum
import Expenses.forms as forms


@login_required(login_url="users:login")
def add_expense(request):
    if request.method == "POST":
        category_id = request.POST.get("category")
        category_obj = (
            Category.objects.filter(id=category_id, user=request.user).first()
            if category_id
            else None
        )
        print(f"Input data - {request.POST}, Category object - {category_obj}")  # Debugging line to check input data and category object
        Transaction.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            amount=Decimal(request.POST.get("amount")),
            transaction_type="expense",  # Hardcoded type for explicit endpoint
            category=category_obj,
        )
    return redirect("users:home")

@login_required(login_url="users:login")
def add_expense_from_form(request):
    return render(request, "add_expense.html", {"form": forms.AddExpenseForm(user=request.user)})

@login_required(login_url="users:login")
def add_expense_from_form_submission(request):
    if request.method == "POST":
        form = forms.AddExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            category = form.cleaned_data["Category"]
            Transaction.objects.create(
                user=request.user,
                title=form.cleaned_data["Title"],
                amount=form.cleaned_data["Amount"],
                transaction_type="expense",
                category=category,
            )
            return redirect("users:home")



@login_required(login_url="users:login")
def add_income(request):
    if request.method == "POST":
        category_id = request.POST.get("category")
        category_obj = (
            Category.objects.filter(id=category_id, user=request.user).first()
            if category_id
            else None
        )

        Transaction.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            amount=Decimal(request.POST.get("amount")),
            transaction_type="income",  # Hardcoded type for explicit endpoint
            category=category_obj,
        )
    return redirect("users:home")


@login_required(login_url="users:login")
def add_category(request):
    if request.method == "POST":
        cat_name = request.POST.get("category_name").strip()
        if cat_name:
            Category.objects.get_or_create(user=request.user, name=cat_name)
    return redirect("users:home")


@login_required(login_url="users:login")
def delete_transaction(request, transaction_id):
    if request.method == "POST":
        transaction = Transaction.objects.filter(
            id=transaction_id, user=request.user
        ).first()
        if transaction:
            transaction.delete()
    return redirect("users:home")

@login_required(login_url="users:login")
def edit_transaction(request, transaction_id):
    if request.method == "PATCH":
        transaction = Transaction.objects.filter(
            id=transaction_id, user=request.user
        ).first()
        if transaction:
            transaction.update()
    return redirect("users:home")


@login_required(login_url="users:login")
def piechart(request):
    current_user = request.user
    today = date.today()

    # Fetching records for the current user and month
    user_txns = (
        Transaction.objects.filter(
            user=current_user,
            date__year=today.year,
            date__month=today.month,
            amount__gt=0,
        )
        .exclude(transaction_type="income")
        .values("category__name")
        .annotate(total_amount=Sum("amount"))
        .order_by("-total_amount")
    )

    print(f"user_txns------{user_txns}")

    labels = [item["category__name"] for item in user_txns]
    amounts = [float(item["total_amount"]) for item in user_txns]

    print(f"labels------{labels}")
    print(f"amounts------{amounts}")

    context = {
        "labels": labels,
        "data_values": amounts,
        "title": "Expense Distribution by Category",
    }
    return render(request, "piechart.html", context)
