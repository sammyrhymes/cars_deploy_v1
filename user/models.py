
from django.db import models
from django.contrib.auth.models import User

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
    

class Wallet(models.Model):
    user = user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, default=0)


    def __str__(self):
        return f'{self.user.username } - {self.amount}'


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

