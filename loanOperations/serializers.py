from rest_framework import serializers
from .models import LoanRequest, LoanInvestorOffers, LoanSubmit, LoanSchedule
from borrower.models import Borrower

from borrower.serializers import BorrowerSerializer
from investor.serializers import InvestorSerializer

