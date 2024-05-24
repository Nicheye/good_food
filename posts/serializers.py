from rest_framework import serializers
from .models import FoodPost, ImagePost
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('host')

class FPost_serializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    class Meta:
        model = FoodPost
        fields = ['title','composition','weight','proteins','fats','carbohydrates','created_at','created_by','id','images']
        extra_kwargs = {
			'images':{'read_only':True}
		}
    def get_images(self,obj):
        images = ImagePost.objects.filter(post=obj)
        ser = Image_serializer(images,many=True)
        return ser.data

    def get_created_by(self,obj):
        return obj.created_by.username

class Image_serializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = ImagePost
        fields = ['image']
    def get_image(self,obj):
        return host + str(obj.image.url)