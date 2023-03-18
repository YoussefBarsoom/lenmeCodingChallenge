from rest_framework import serializers
from .models import Investor
from .models import Borrower
from .models import Offer

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields=['id','name','amount']

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields=['id','name']

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields=['id','borrowerId','investorId','loanAmount','loanPeriod','annualRate','status','startDate','monthsPaid']