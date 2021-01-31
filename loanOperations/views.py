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


# To display the all borrower loan requests
@api_view(['GET'])
def detailRequestBorrower(request, pk):
	try:
		borrower = Borrower.objects.get(id=pk)          # query borroer using ID.
	except ObjectDoesNotExist:                          # if borrower dosn't exist
		return Response("Sorry! You aren't register, Please create a new account", status=status.HTTP_401_UNAUTHORIZED)

	loan_request = LoanRequest.objects.filter( Q(Id_borrower=pk)).values()  # query all request related to borrower
	if(loan_request.exists()):
		return Response(querySet_to_list(loan_request))
	else:
		return Response("There aren't loan requests yet", status=status.HTTP_404_NOT_FOUND)
