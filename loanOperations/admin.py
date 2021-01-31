from django.contrib import admin
from .models import LoanRequest, LoanInvestorOffers, LoanSubmit, LoanSchedule
# Register your models here.

admin.site.register(LoanRequest)
admin.site.register(LoanInvestorOffers)
admin.site.register(LoanSubmit)
admin.site.register(LoanSchedule)

