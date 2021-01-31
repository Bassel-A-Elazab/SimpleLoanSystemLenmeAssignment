from django.db import models

# Create your models here.
class Borrower(models.Model):
    username = models.CharField(max_length=150)
    mail = models.CharField(max_length=150)
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
