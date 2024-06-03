from django.urls import path
from .views import Payments_View,payment_admin,approve_payment,decline_payment

urlpatterns = [
    path('',Payments_View.as_view(),name="payments"),
    path('admin',payment_admin,name="payments_admin"),
    path('approve_payment/<int:id>',approve_payment,name="approve_payment"),
    path('decline_payment/<int:id>',decline_payment,name="decline_payment"),
]
