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

# for handle all offers from investor to each borrower
class LoanInvestorOffers(models.Model):
    Id_investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    Id_loan_request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE)

# for handle all accept offers from borrower after investors offer and calculte the payment amount also notice borrower for payment date.
class LoanSubmit(models.Model):
    Id_borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    Id_investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    Id_loan_request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE)
    amount_per_date = models.FloatField()
    date1 = models.DateField() 
    date2 = models.DateField()
    date3 = models.DateField()
    date4 = models.DateField()
    date5 = models.DateField()
    date6 = models.DateField()

# for creating a scheduling for payment borrower across the specidied period (6 months) also to handle the completed re-payment for investor
class LoanSchedule(models.Model):
    Id_submit = models.ForeignKey(LoanSubmit, on_delete=models.CASCADE)
    payment1 = models.BooleanField(default=False)
    payment2 = models.BooleanField(default=False)
    payment3 = models.BooleanField(default=False)
    payment4 = models.BooleanField(default=False)
    payment5 = models.BooleanField(default=False)
    payment6 = models.BooleanField(default=False)


