from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    gender = models.CharField(max_length=15, default='man')
    birth_date = models.DateTimeField(default=timezone.now)
    country = models.CharField(max_length=50, default='kz')
    city = models.CharField(max_length=50, default='astana')
    higher_education = models.CharField(max_length=100, default='no')

    def __str__(self):
        return f"{self.user.username} Profile"

