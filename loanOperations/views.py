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
	
	loanSubmit = LoanSubmit.objects.filter( Q(Id_investor=pk_investor),  Q(Id_loan_request=pk_loan))  # query the specific submitted loan
	if(loanSubmit.exists()):                                # check if the loan request submitted before.
		return Response("Sorry! This request fundedd before", status=status.HTTP_400_BAD_REQUEST)

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

# To allow borrower for accepting  the investor's offer of the loan request.
@api_view(['GET'])
def acceptOffer(request, pk_borrower, pk_loan, pk_investor):
	try:
		borrower = Borrower.objects.get(id=pk_borrower)         # check if the borrower dosn't exisit.
	except ObjectDoesNotExist:
		return Response("Sorry! You aren't register, Please create a new account", status=status.HTTP_401_UNAUTHORIZED)

	try:
		investor = Investor.objects.get(id=pk_investor)                 #check of investor exist to validate passing data.
	except ObjectDoesNotExist:
		return Response("Sorry! Invalid investor choosing, Please, Choose the correct investor", status=status.HTTP_400_BAD_REQUEST)

	try:
		loanRequest = LoanRequest.objects.get(id=pk_loan)               # check if the loan request dosn't exisit of fundded or input unvalid data.
	except ObjectDoesNotExist:
		return Response("Sorry! Invalid loan request choosing, Please, Choose correct loan request", status=status.HTTP_400_BAD_REQUEST)

	loanSubmit = LoanSubmit.objects.filter( Q(Id_borrower=pk_borrower),  Q(Id_loan_request=pk_loan))  # query the specific submitted loan
	if(loanSubmit.exists()):                                # check if the loan request submitted before.
		return Response("Sorry! This request fundedd before", status=status.HTTP_400_BAD_REQUEST)
	
	investor_offer = LoanInvestorOffers.objects.filter(Q(Id_loan_request=pk_loan))

	annual_rate_half = 0.075                # to calculate the half annual rate (6 months) paid.
	payPeriods = []                         # assing the 6 period for payment.
	
	# To update balance
	checkForBalance = investor.balance - (loanRequest.amount+3) 
	if(investor.balance >= checkForBalance):                      #check if investor balance enough for (payment+lenme fee)
		investor.balance = checkForBalance

	investorSerializer = InvestorSerializer(instance=investor, data=request.data,partial=True)
	if investorSerializer.is_valid():
		investorSerializer.save()

	# To update status of request
	loanRequest.status = "funded"                               # updated tha status of the loan request after borrower accpet the offer.
	loanSerializer = LoanRequestSerializer(instance=loanRequest, data=request.data, partial=True)
	if loanSerializer.is_valid():
		loanSerializer.save()

	amount_per_date = ((loanRequest.amount+3) * annual_rate_half) / 6.0          # calculate the amount that will pay in each date for (6 months).
	payPeriods = scheduled_date()

	request.data["amount_per_date"] = amount_per_date
	for i in range(6):
		request.data["date"+str(i+1)] = payPeriods[i]
	
	loanSubmitSerializer = LoanSubmitSerializer(data=request.data)

	if loanSubmitSerializer.is_valid():             
		# Submitted offers
		loanSubmitSerializer.validated_data["Id_borrower_id"] =  borrower.id
		loanSubmitSerializer.validated_data["Id_investor_id"] =  investor.id
		loanSubmitSerializer.validated_data["Id_loan_request_id"] =  loanRequest.id
		loanSubmitSerializer.save()

		# Schedule Payment for borrower
		loanScheduleSerializer = LoanScheduleSerializer(data=request.data)
		if(loanScheduleSerializer.is_valid()):
			loanScheduleSerializer.validated_data["Id_submit_id"] = loanSubmitSerializer.data["id"]
			loanScheduleSerializer.save()
					# Delete a loan request from offers
			investor_offer.delete()              
			return Response("Scheduled payment created successfully, Please following your payments date", status=status.HTTP_201_CREATED)
	return Response("Sorry, Please Enter valid data", status=status.HTTP_400_BAD_REQUEST)

# for converting the QuerySet return by objects into list to be able to display it.
def querySet_to_list(qs):
    return [dict(q) for q in qs]

# set the scheduled for 6 months to assignit for borrower.
def scheduled_date():
	scheduled_date = []
	scheduled_date.append(date.today() + relativedelta(months=+1))
	for i in range(1,6):
		scheduled_date.append(scheduled_date[i-1]+relativedelta(months=+1))
	return scheduled_date

@api_view(['GET'])
def getAllLoanSubmitted(request, pk_borrower):
	try:
		borrower = Borrower.objects.get(id=pk_borrower)             # check if the borrower dosn't exisit.
	except ObjectDoesNotExist:
		return Response("Sorry! You aren't register, Please create a new account", status=status.HTTP_401_UNAUTHORIZED)

	loanSubmit = LoanSubmit.objects.filter( Q(Id_borrower=pk_borrower)).values()
	if loanSubmit.exists():                 # display all offers from investor to borrower.
		return Response(querySet_to_list(loanSubmit))
	return Response("Sorry! There aren't loan submitted yet", status=status.HTTP_404_NOT_FOUND)
