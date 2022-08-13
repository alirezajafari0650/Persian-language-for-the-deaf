from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = PhoneNumberField(unique=True)
    is_profetional = models.BooleanField(default=False)

    def __str__(self):
        string = self.first_name + ' ' + self.last_name
        if len(string) != 1:
            return string
        else:
            return str(self.username)


class Ad(models.Model):
    description = models.TextField()
