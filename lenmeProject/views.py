from django.http import JsonResponse
from .models import Investor
from .models import Offer

from .models import Borrower
from .serializers import InvestorSerializer
from .serializers import BorrowerSerializer
from .serializers import OfferSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date
import pandas as pd

@api_view(['GET','POST'])
def investor_list(request):

    if request.method == 'GET':
        investors = Investor.objects.all()
        serializer = InvestorSerializer(investors,many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer= InvestorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET','POST'])
def borrower_list(request):

    if request.method == 'GET':
        borrowers = Borrower.objects.all()
        serializer = BorrowerSerializer(borrowers,many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer= BorrowerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)


@api_view(['GET','POST'])
def offer_list(request):

    if request.method == 'GET':
        offers = Offer.objects.all()
        serializer = OfferSerializer(offers,many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        output={
            "borrowerId":request.data['borrowerId'],
            "loanAmount":request.data['loanAmount'],
            "loanPeriod":request.data['loanPeriod'],
            "status":"Pending"
        }
        serializer= OfferSerializer(data=output)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def acceptOffer(request,id):

    if request.method == 'PUT':
        try:
            offerObj=Offer.objects.get(pk=id)
        except Offer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # output=offerObj
        # offerObj.investorId=request.data['investorId']
        # offerObj.annualRate=request.data['annualRate']
        # offerObj.status="Proposal Pending"
        today = date.today()

        output={
            "id":offerObj.id,
            "borrowerId":offerObj.borrowerId.id,
            "loanAmount":offerObj.loanAmount,
            "loanPeriod":offerObj.loanPeriod,
            "investorId":offerObj.investorId.id,
            "annualRate":offerObj.annualRate,

            "status":"Funded",
            "startDate":today,
            "monthsPaid":0
            ,"ad":"add"
            }
        # output={offerObj,"status"="Proposal Pending","investorId"=request.data['investorId'],"annualRate"=request.data['annualRate']}
        serializer= OfferSerializer(offerObj,data=output)
        if serializer.is_valid():
            serializer.save()
            monthlyPayment=(offerObj.loanAmount*(1+(offerObj.annualRate/100)))/offerObj.loanPeriod
            dates=[]
            for i in range(0,offerObj.loanPeriod):
                new_date = pd.to_datetime(today)+pd.DateOffset(months=i)
                dates.append(str(new_date))
            return Response({"monthlyPayment":monthlyPayment,"dates":dates},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])

def payInstallment(request,id):

    if request.method == 'PUT':
        try:
            offerObj=Offer.objects.get(pk=id)
        except Offer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if offerObj.monthsPaid+1==offerObj.loanPeriod:
            if offerObj.status!="Completed":
                output={
            "id":offerObj.id,
            "borrowerId":offerObj.borrowerId.id,
            "loanAmount":offerObj.loanAmount,
            "loanPeriod":offerObj.loanPeriod,
            "investorId":offerObj.investorId.id,
            "annualRate":offerObj.annualRate,
            "status":"Completed",
            "startDate":offerObj.startDate,

            "monthsPaid":offerObj.monthsPaid+1
            }
            else:
        
                output={
            "id":offerObj.id,
            "borrowerId":offerObj.borrowerId.id,
            "loanAmount":offerObj.loanAmount,
            "loanPeriod":offerObj.loanPeriod,
            "investorId":offerObj.investorId.id,
            "annualRate":offerObj.annualRate,
            "status":offerObj.status,
            "startDate":offerObj.startDate,

            "monthsPaid":offerObj.monthsPaid+1
            }    
        
        # output={offerObj,"status"="Proposal Pending","investorId"=request.data['investorId'],"annualRate"=request.data['annualRate']}
            serializer= OfferSerializer(offerObj,data=output)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"Loan is Completed"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])

def proposeRate(request):
    lenmeFee=3
    if request.method == 'PUT':
        try:
            offerObj=Offer.objects.get(pk=request.data["offerId"])
        except Offer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # output=offerObj
        # offerObj.investorId=request.data['investorId']
        # offerObj.annualRate=request.data['annualRate']
        # offerObj.status="Proposal Pending"
        try:
            investorObj=Investor.objects.get(pk=request.data["investorId"])
        except Offer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if investorObj.amount>=(offerObj.loanAmount+lenmeFee):

            output={
            "id":offerObj.id,
            "borrowerId":offerObj.borrowerId.id,
            "loanAmount":offerObj.loanAmount,
            "loanPeriod":offerObj.loanPeriod,
            "investorId":request.data['investorId'],
            "annualRate":request.data['annualRate'],
            "status":"Proposal Pending"        
            }
        # output={offerObj,"status"="Proposal Pending","investorId"=request.data['investorId'],"annualRate"=request.data['annualRate']}
            serializer= OfferSerializer(offerObj,data=output)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Insufficient Balance in Investor's account to cover total loan amount."},status=status.HTTP_400_BAD_REQUEST)


    
    



@api_view(['GET','PUT','DELETE'])
def investor_details(request,id):

    try:
        investorObj=Investor.objects.get(pk=id)
    except Investor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer = InvestorSerializer(investorObj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method=='PUT':
        serializer = InvestorSerializer(investorObj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    elif request.method=='DELETE':
        investorObj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

