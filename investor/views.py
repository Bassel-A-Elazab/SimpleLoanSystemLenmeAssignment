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

