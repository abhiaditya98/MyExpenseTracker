from django import forms
from Expenses.models import Category


class AddExpenseForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        required=True,
        label="Expense Title",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Swiggy, Rent, Petrol..."}
        ),
    )

    amount = forms.DecimalField(
        min_value=0.01,
        max_digits=100000,
        decimal_places=2,
        required=True,
        label="Amount",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter amount",
                "id": "id_amount",
            }
        ),
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=True,
        label="Category",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # Overriding __init__ to filter based on the logged-in user
    def __init__(self, *args, **kwargs):
        # Extract the user from the keyword arguments [1]
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # If a user is provided, filter the category queryset [1]
        if user:
            # Replace 'user' with whatever the ForeignKey field name is on your Category model [1]
            self.fields["category"].queryset = Category.objects.filter(user=user)
