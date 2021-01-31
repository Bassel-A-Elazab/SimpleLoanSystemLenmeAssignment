from django.urls import path
from . import views

urlpatterns = [
    path('borrower-create/', views.borrowerCreate, name="borrower-create"),
	path('borrower-detail/<str:pk>/', views.borrowerDetail, name="borrower-detail"),
	path('borrower-update/<str:pk>/', views.borrowerUpdate, name="borrower-update"),
	path('borrower-delete/<str:pk>/', views.borrowerDelete, name="borrower-delete"),
]
