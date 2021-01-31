from django.urls import path
from . import views

urlpatterns = [
    path('borrower/<str:pk>/loan_request', views.loanRequest_create, name="loan-request"),
    path('borrower/<str:pk>/list_request', views.detailRequestBorrower, name="list-request"),
    path('borrower/<str:pk_borrower>/request_offers/<str:pk_loan>', views.detailRequestBorrowerOffers, name="list-request-offers"),
    path('borrower/<str:pk_borrower>/list_request/<str:pk_loan>/accept_offer/<str:pk_investor>', views.acceptOffer, name="accept-offer"),

    path('investor/<str:pk>/list_loan', views.detailRequestsForInvestor, name="list-loan-request"),
    path('investor/<str:pk_investor>/offer/<str:pk_loan>', views.createOfferLoan, name="Offer-loan-request"),
]
