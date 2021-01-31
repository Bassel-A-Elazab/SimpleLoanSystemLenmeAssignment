from django.urls import path
from . import views

urlpatterns = [
    path('investor-create/', views.investorCreate, name="investor-create"),
	path('investor-detail/<str:pk>/', views.investorDetail, name="investor-detail"),
	path('investor-update/<str:pk>/', views.investorUpdate, name="investor-update"),
	path('investor-delete/<str:pk>/', views.investorDelete, name="investor-delete"),
]
