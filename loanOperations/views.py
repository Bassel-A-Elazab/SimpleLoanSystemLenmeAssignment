from datetime import date
from dateutil.relativedelta import relativedelta

from django.shortcuts import render
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import LoanRequest, LoanInvestorOffers, LoanSubmit, LoanSchedule
from borrower.models import Borrower
from investor.models import Investor
from investor.serializers import InvestorSerializer

from .serializers import LoanRequestSerializer, LoanInvestoroffersSerializer, LoanSubmitSerializer, LoanScheduleSerializer






