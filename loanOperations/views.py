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
	except ObjectDoesNotExist:                          # if borrower dosn't exist.
		return Response("Sorry! You aren't register, Please create a new account", status=status.HTTP_401_UNAUTHORIZED)

	loan_request = LoanRequest.objects.filter( Q(Id_borrower=pk)).values()  # query all request related to borrower.
	if(loan_request.exists()):
		return Response(querySet_to_list(loan_request))
	else:
		return Response("There aren't loan requests yet", status=status.HTTP_404_NOT_FOUND)

#  Borrower request for loan.
@api_view(['POST'])
def loanRequest_create(request,pk):
	try:
		borrower = Borrower.objects.get(id=pk)      # check if borrower exist first.
	except ObjectDoesNotExist:                      #handle exception if isn't exist and return 401 unauthoized
		return Response("Sorry! You aren't register, Please create a new account", status=status.HTTP_401_UNAUTHORIZED)
	
	request.data["Id_borrower"] = borrower.id
	loanRequest = LoanRequestSerializer(data=request.data)
	
	if loanRequest.is_valid():          # save a request of loan related with borrower that ask for it.
		loanRequest.validated_data["Id_borrower_id"] =  borrower.id
		loanRequest.save()
		return Response("Successfully, Please waiting for an offer from one of the investors", status=status.HTTP_201_CREATED)
	return Response("Sorry, Please Enter valid data", status=status.HTTP_400_BAD_REQUEST)


# Display all loan request for investor to offer what they want to payment.
@api_view(['GET'])
def detailRequestsForInvestor(request,pk):
	try:
		investor = Investor.objects.get(id=pk)          #check of investor exist to validate passing data.
	except ObjectDoesNotExist:
		return Response("Sorry! You aren't register, Please create a new account", status=status.HTTP_401_UNAUTHORIZED)
	
	loan_request = LoanRequest.objects.filter(status="null")            # query all requests that isn't funded yet.
	if(loan_request.exists()):                              
		serializer = LoanRequestSerializer(loan_request, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)         # response the all loan request to investor.
	else:
		return Response("There aren't loan requests yet", status=status.HTTP_404_NOT_FOUND)


# Creates new offer from investors to the borrower's loan requests.
@api_view(['GET'])
def createOfferLoan(request, pk_investor, pk_loan):

	investorOffer = LoanInvestorOffers.objects.filter( Q(Id_investor=pk_investor),  Q(Id_loan_request=pk_loan))    # check if you resubmit the same offer.
	if(investorOffer.exists()):
		return Response("Sorry! You offered this request before", status=status.HTTP_400_BAD_REQUEST)

	try:
		investor = Investor.objects.get(id=pk_investor)     # check if unauthorized investor offer payment to borrower.
	except ObjectDoesNotExist:
		return Response("Sorry! You aren't register, Please create a new account", status=status.HTTP_401_UNAUTHORIZED)

	try:
		loan_request = LoanRequest.objects.get(id=pk_loan)      # chek if the loan dosn't exisit or investor enter valid data.
	except ObjectDoesNotExist:
		return Response("Sorry! Invalid loan request, Please enter valid loan request", status=status.HTTP_400_BAD_REQUEST)
	
	serializer = LoanInvestoroffersSerializer(data=request.data)
	if serializer.is_valid():                           # save the investor with offering the loan request to able borrower to see it.
		serializer.validated_data["Id_investor_id"] =  investor.id
		serializer.validated_data["Id_loan_request_id"] =  loan_request.id
		serializer.save()
		return Response(serializer.data)
	return Response(serializer.errors)


# to display all investor offers to the borrower's loan request.
@api_view(['GET'])
def detailRequestBorrowerOffers(request, pk_borrower, pk_loan):
	try:
		borrower = Borrower.objects.get(id=pk_borrower)             # check if the borrower dosn't exisit.
	except ObjectDoesNotExist:
		return Response("Sorry! You aren't register, Please create a new account", status=status.HTTP_401_UNAUTHORIZED)

	try:
		loanRequest = LoanRequest.objects.get(id=pk_loan)           # check if the loan request dosn't exisit of fundded or input unvalid data.
	except ObjectDoesNotExist:
		return Response("Sorry! There aren't loan requests yet", status=status.HTTP_404_NOT_FOUND)
	
	investor_offer = LoanInvestorOffers.objects.filter( Q(Id_loan_request=pk_loan)).values()
	if investor_offer.exists():                 # display all offers from investor to borrower.
		return Response(querySet_to_list(investor_offer))
	return Response("Sorry! There aren't any offers from investors yet \n Please, Waiting for investor offers", status=status.HTTP_404_NOT_FOUND)


