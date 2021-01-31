from rest_framework import serializers
from .models import LoanRequest, LoanInvestorOffers, LoanSubmit, LoanSchedule
from borrower.models import Borrower

from borrower.serializers import BorrowerSerializer
from investor.serializers import InvestorSerializer

# for loan request module
class LoanRequestSerializer(serializers.ModelSerializer):
	Id_borrower = BorrowerSerializer(read_only=True)
	
	class Meta:	
		model = LoanRequest
		fields ='__all__'

# for invesotr offer module
class LoanInvestoroffersSerializer(serializers.ModelSerializer):
	Id_investor = InvestorSerializer(read_only=True)
	Id_loan_request = LoanRequestSerializer(read_only=True)
	class Meta:	
		model = LoanInvestorOffers
		fields ='__all__'

# for loan submitted module
class LoanSubmitSerializer(serializers.ModelSerializer):
	Id_borrower = BorrowerSerializer(read_only=True)
	Id_investor = InvestorSerializer(read_only=True)
	Id_loan_request = LoanRequestSerializer(read_only=True)
	class Meta:	
		model = LoanSubmit
		fields ='__all__'

# for scheduled module 
class LoanScheduleSerializer(serializers.ModelSerializer):
	Id_submit = LoanSubmitSerializer(read_only=True)
	class Meta:	
		model = LoanSchedule
		fields ='__all__'
