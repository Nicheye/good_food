from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Report,Ticket
from posts.serializers import FPost_serializer
class Report_Serializer(ModelSerializer):
    created_by = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    class Meta:
        model = Report
        fields = ['post','description','created_by','created_at','status','message']
        extra_kwargs = {
			'message':{'read_only':True}
		}
    def get_created_by(self,obj):
        return obj.created_by.username

    def get_post(self,obj):
        user_ser = FPost_serializer(obj.post)
        return user_ser.data

class Ticket_Serializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['reason','description','created_by','created_at','status','respond']
        extra_kwargs = {
			'respond':{'read_only':True}
		}
