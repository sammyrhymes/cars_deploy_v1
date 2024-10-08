
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(default='avatar.jpg', upload_to='Profile_Images')
    # New fields for the competition
    date_of_birth = models.DateField(null=True, blank=True)
    favorite_car = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - Profile'
    

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Ticket Purchase', 'Ticket Purchase'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} KES"
    

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)

    def __str__(self):
        return f'{self.user.username} - {self.amount}'

    def update_balance(self, amount_change, transaction_type):
        """Update the wallet balance and create a transaction."""
        try:
            amount_change = Decimal(amount_change)

            # Update the wallet's amount
            self.amount += amount_change
            self.save()  # Save the updated wallet
            
            # Create a transaction record
            Transaction.objects.create(
                user=self.user,
                transaction_type=transaction_type,
                amount=amount_change,
            )
        except Exception as e:
            print(f"Error while updating balance or creating transaction: {e}")


