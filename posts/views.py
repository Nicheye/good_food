from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import FPost_serializer,Image_serializer
from .models import FoodPost,ImagePost
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .tasks import calculate_usefulness
from authentification .models import User,Profile
from authentification .serializers import UserSerializer,ProfileSerializer


class Lenta_View(ListAPIView):
    serializer_class = FPost_serializer
    queryset = FoodPost.objects.order_by('-created_at')


class Post_View(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        if id is None:
            return Response({'message': "You haven't provided an ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        post_obj = get_object_or_404(FoodPost, id=id)
        ser = FPost_serializer(post_obj)
        return Response({'data': ser.data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        user = request.user

        post_ser = FPost_serializer(data=data)
        post_ser.is_valid(raise_exception=True)
        post_obj = post_ser.save(created_by=user)
        post_obj.ben_koef = calculate_usefulness(post_obj)
        post_obj.save()
        return Response({'post': post_ser.data}, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        id = kwargs.get("id")
        if id is None:
            return Response({'message': "You haven't provided an ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        post_obj = get_object_or_404(FoodPost, id=id)

        # Check if the user is the owner of the post (or has permission to edit it)
        if post_obj.created_by != user:
            return Response({'message': "You do not have permission to edit this post"}, status=status.HTTP_403_FORBIDDEN)

        if 'images' in data and data['images']:
            images = data['images']
            for image in images:
                ImagePost.objects.create(post=post_obj, image=image)
        
        if 'is_public' in data:
            post_obj.is_public = data['is_public']
            post_obj.save()

        post_ser = FPost_serializer(post_obj)
        return Response({'post': post_ser.data, 'message': 'Post updated successfully'}, status=status.HTTP_202_ACCEPTED)


class Profile_View(APIView):
    
    permission_classes= [IsAuthenticatedOrReadOnly]

    def get(self,request,*args,**kwargs):
        id = kwargs.get("id",None)
        if id is not None:
            user_obj = get_object_or_404(FoodPost,id=id)
            if user_obj:
                user_ser = UserSerializer(user_obj)                
                posts = FoodPost.objects.filter(created_by=user_obj,is_public=True)
                posts_ser =FPost_serializer(posts,many=True)
                return Response({'data':user_ser.data,'posts':posts_ser.data},status=status.HTTP_200_OK)
        user_obj =request.user
        user_ser = UserSerializer(request.user)
        posts = FoodPost.objects.filter(created_by=user_obj)
        posts_ser =FPost_serializer(posts,many=True)
        return Response({'data':user_ser.data,'posts':posts_ser.data},status=status.HTTP_200_OK)
    
        
    
    def patch(self,request):
        data = request.data
        user = request.user

        profile_ser = ProfileSerializer(data=data)
        avatar = request.FILES.get('avatar')
        if profile_ser.is_valid(raise_exception=True):
            if avatar is not None:
                profile_ser.save(avatar=avatar)
            profile_ser.save()
            return Response({'data':profile_ser.data},status=status.HTTP_205_RESET_CONTENT)
    
    
class Settings_View(APIView):
    
    def patch(self,request):
        try:
            user_obj = request.user
            data = request.data
            changes = 0
            if 'username' in data and data['username'] != '':
                user_obj.username = data['username']
                changes =1
            if 'email' in data and data['email'] != '':
                user_obj.email = data['email']
                changes =1
            if changes ==1:
                user_obj.save()
            user_ser = UserSerializer(user_obj)
            return Response({'data':user_ser.data},status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'error'},status=status.HTTP_400_BAD_REQUEST)


    

        


