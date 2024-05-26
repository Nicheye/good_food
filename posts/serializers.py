from rest_framework import serializers
from .models import FoodPost, ImagePost,Like
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('host')



class FPost_serializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = FoodPost
        fields = ['title', 
                  'composition', 
                  'weight', 
                  'proteins', 
                  'fats', 
                  'carbohydrates', 
                  'created_at', 
                  'created_by', 
                  'id', 
                  'cat', 
                  'is_public', 
                  'images', 
                  'likes', 
                  'is_liked']
        extra_kwargs = {
            'images': {'read_only': True}
        }

    def get_images(self, obj):
        images = ImagePost.objects.filter(post=obj)
        ser = Image_serializer(images, many=True)
        return ser.data

    def get_created_by(self, obj):
        return obj.created_by.username

    def get_is_liked(self, obj):
        try:
            request = self.context.get('request', None)
            if request and request.user.is_authenticated:
                return Like.objects.filter(post=obj, liked_by=request.user).exists()
            return False
        except:
            return False


class Image_serializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = ImagePost
        fields = ['image']
    def get_image(self,obj):
        return host + str(obj.image.url)

class Like_serializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ['post','liked_by']
    
    def get_post(self,obj):
        post_obj = FoodPost.objects.get(id=obj.post.id)
        post_ser = FPost_serializer(post_obj)
        return post_ser.data
    def get_liked_by(self,obj):
        return str(obj.liked_by.username)

