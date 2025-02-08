from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Chat(models.Model):
    message = models.CharField(max_length=12000)
    image = models.ImageField(upload_to="images/")

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    username = None  # Remove username

    USERNAME_FIELD = "email"  # Use email as the unique identifier
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    def __str__(self):
        return self.email