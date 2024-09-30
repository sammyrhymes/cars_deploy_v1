
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

