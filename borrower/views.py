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
	return Response("Congratulation to Lenme", status=status.HTTP_201_CREATED)


