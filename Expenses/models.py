from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='categories'
    )
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"
        # Prevents a single user from creating duplicate categories
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='transactions'
    )
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    
    # Links to your dynamic Category model
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='transactions'
    )
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']  # Shows newest transactions first by default

    def __str__(self):
        return f"{self.title} ({self.transaction_type}) - ₹{self.amount}"
