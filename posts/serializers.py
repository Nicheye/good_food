from rest_framework import serializers
from .models import FoodPost, ImagePost,Like,Comment,Bookmark,UsefulnessHistory
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('host')



from rest_framework import serializers
from .models import FoodPost, ImagePost, Like

from rest_framework import serializers
from .models import FoodPost, ImagePost, Like

class FPost_serializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = FoodPost
        fields = [
            'title', 'composition', 'weight', 'proteins', 'fats', 
            'carbohydrates', 'created_at', 'created_by', 'id', 
            'cat', 'is_public', 'images', 'likes', 'is_liked',
            'comments','sugar','calories','ben_koef'
        ]
        extra_kwargs = {
            'images': {'read_only': True},
            'title': {'required': False},
            'composition': {'required': False},
            'proteins': {'read_only': True},
            'fats': {'read_only': True},
            'carbohydrates': {'read_only': True},
            'sugar': {'read_only': True},
            'calories': {'read_only': True},
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


class Comment_serializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    commented_by = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['post','message','commented_by']
    
    def get_post(self,obj):
        post_obj = FoodPost.objects.get(id=obj.post.id)
        post_ser = FPost_serializer(post_obj)
        return post_ser.data
    def get_commented_by(self,obj):
        return str(obj.commented_by.username)
    
class Bookmark_serializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    marked_by = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = ['post','marked_by']
    
    def get_post(self,obj):
        post_obj = FoodPost.objects.get(id=obj.post.id)
        post_ser = FPost_serializer(post_obj)
        return post_ser.data
    def get_marked_by(self,obj):
        return str(obj.marked_by.username)


class UsefulnessHistorySerializer(serializers.ModelSerializer):
    day = serializers.DateField()
    avg_ben_koef = serializers.FloatField()

    class Meta:
        model = UsefulnessHistory
        fields = ['day', 'avg_ben_koef']

