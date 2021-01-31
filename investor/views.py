from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import InvestorSerializer
from .models import Investor

# Create your views here.
@api_view(['GET'])
def apiOverview1(request):
	api_urls = {
		'Create':'/Investor-create/',
        'Detail Investor':'/Investor-detail/<str:pk>/',
		'Update':'/Investor-update/<str:pk>/',
		'Delete':'/Investor-delete/<str:pk>/',
		}
	return Response(api_urls)

# Create a new Investor
@api_view(['POST'])
def investorCreate(request):
	investor = InvestorSerializer(data=request.data)
	if investor.is_valid():
		investor.save()
	return Response(investor.data)

# Dsiplay investor information
@api_view(['GET'])
def investorDetail(request,pk):
	try:
		investor = Investor.objects.get(id=pk)
	except ObjectDoesNotExist:
		return Response("Sorry! You aren't register, Please create a new account", status=status.HTTP_401_UNAUTHORIZED)
		
	serializer = InvestorSerializer(investor, many=False)
	return Response(serializer.data, status=status.HTTP_200_OK)

# Update an existing borrower
@api_view(['POST'])
def investorUpdate(request, pk):
	try:
		investor = Investor.objects.get(id=pk)
	except ObjectDoesNotExist:
		return Response("Sorry! You aren't register, Please create a new account", status=status.HTTP_401_UNAUTHORIZED)

	serializer = InvestorSerializer(instance=investor, data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response("Your information updated successfully", status=status.HTTP_200_OK)
