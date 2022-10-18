from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = PhoneNumberField(unique=True)
    is_professional = models.BooleanField(default=False)

    def __str__(self):
        string = self.first_name + ' ' + self.last_name
        if len(string) != 1:
            return string
        else:
            return str(self.username)


class Ad(models.Model):
    description = models.TextField()


class Facture(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ' ' + str(self.price)
