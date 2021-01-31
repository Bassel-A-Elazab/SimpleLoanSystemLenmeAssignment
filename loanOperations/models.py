from django.db import models
from borrower.models import Borrower
from investor.models import Investor

# Create your models here.

# for handle all borrower loan requests and their status
class LoanRequest(models.Model):
    Id_borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    amount = models.FloatField()
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, default="null")

