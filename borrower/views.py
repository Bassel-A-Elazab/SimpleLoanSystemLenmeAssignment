from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Borrower
from .serializers import BorrowerSerializer

# Create your views here.
@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'Create':'/borrower-create/',
        'Detail borrower':'/borrower-detail/<str:pk>/',
		'Update':'/borrower-update/<str:pk>/',
		'Delete':'/borrower-delete/<str:pk>/',
		}
	return Response(api_urls)

# Create a new Borrower
@api_view(['POST'])
def borrowerCreate(request):
	serializer = BorrowerSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response("Congratulation! Welcome to Lenme", status=status.HTTP_201_CREATED)

# Detail Borrower information
@api_view(['GET'])
def borrowerDetail(request,pk):
	try:
		borrower = Borrower.objects.get(id=pk)
	except ObjectDoesNotExist:
		return Response("Sorry! You aren't register, Please create a new account", status=status.HTTP_401_UNAUTHORIZED)
	serializer = BorrowerSerializer(borrower, many=False)
	return Response(serializer.data, status=status.HTTP_200_OK)

# Update borrower existing information
@api_view(['POST'])
def borrowerUpdate(request, pk):
	try:
		borrower = Borrower.objects.get(id=pk)
	except ObjectDoesNotExist:
		return Response("Sorry! You aren't register, Please create a new account", status=status.HTTP_401_UNAUTHORIZED)
	serializer = BorrowerSerializer(instance=borrower, data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response("Your information updated successfully", status=status.HTTP_200_OK)

# Delete borrower information
@api_view(['DELETE'])
def borrowerDelete(request, pk):
	try:
		borrower = Borrower.objects.get(id=pk)
	except ObjectDoesNotExist:
		return Response("Sorry! You aren't register, Please create a new account", status=status.HTTP_401_UNAUTHORIZED)

	borrower.delete()
	return Response('Item succsesfully delete!', status=status.HTTP_200_OK)
