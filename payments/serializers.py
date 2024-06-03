from rest_framework.serializers import ModelSerializer
from .models import Payment
class Payment_serializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ['user','status','created_at']
