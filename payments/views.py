from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .models import Payment
from .serializers import Payment_serializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from authentification.models import User,Profile

class Payments_View(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        user =request.user
        payments_query = Payment.objects.filter(user=user)
        payments_ser = Payment_serializer(payments_query,many=True)
        return Response({'data':payments_ser.data},status=status.HTTP_302_FOUND)
    
    def post(self,request):
        user = request.user
        thirty_days_ago = timezone.now() - timedelta(days=30)
        payment_exists = Payment.objects.filter(user=user, created_at__gte=thirty_days_ago).exists()
        if payment_exists:
            return Response({'message':"you have already sent a request, wait for confirmation"},status=status.HTTP_400_BAD_REQUEST)
        payment_obj = Payment.objects.create(user=user)
        payment_ser= Payment_serializer(payment_obj)
        return Response({'data':payment_ser.data},status=status.HTTP_201_CREATED)

def payment_admin(request):
    user = request.user
    if user.is_superuser==True:
        payment_requests = Payment.objects.filter(status='pending')
        return render(request,"requests.html",{"requests":payment_requests})
def approve_payment(request,id):
    payment_obj = Payment.objects.get(id=id)
    if payment_obj:
        profile = Profile.objects.get(user=payment_obj.user)
        profile.account_type = 'premium'
        profile.save()
        payment_obj.status = 'approved'
        payment_obj.save()

    return redirect("payments_admin")

def decline_payment(request,id):
    payment_obj = Payment.objects.get(id=id)
    if payment_obj:
       
        payment_obj.status = 'declined'
        payment_obj.save()
        
    return redirect("payments_admin")
