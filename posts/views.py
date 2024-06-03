from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import FPost_serializer, Image_serializer, Like_serializer,Comment_serializer,Bookmark_serializer
from .models import FoodPost, ImagePost, Like,Bookmark
from authentification.models import User, Profile
from authentification.serializers import UserSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .tasks import recommended_posts,get_daily_avg_ben_koef,get_advice,most_popular
from rest_framework import filters
class Lenta_View(ListAPIView):
    serializer_class = FPost_serializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
        })
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return recommended_posts(self.request.user)
        else:
            return most_popular()


class Separated_lenta(APIView):
    def get(self,request,*args,**kwargs):
        filter = kwargs.get('filter',None)
        if filter is None:
            return Response({'message':'you havent provided a filter'},status=status.HTTP_400_BAD_REQUEST)
        
        cats_keywords = {
        'losing': 'похудение',
        'sport': 'спортпит',
        'vegan': 'веган',
        'health': 'здоровье',
        'anti_age':'анти-Эйджинг',
        'family':'семья',
        'med':'мед'
         }
        for eng, rus in cats_keywords.items():
            if eng in filter:
                posts_query = FoodPost.objects.filter(cat=rus).order_by('likes')
                posts_ser = FPost_serializer(posts_query,many=True)
                return Response({'data':posts_ser.data},status=status.HTTP_302_FOUND)
        if filter == 'popular':
            posts_query = most_popular
            posts_ser = FPost_serializer(posts_query,many=True)
            return Response({'data':posts_ser.data},status=status.HTTP_302_FOUND)
        


class Post_View(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        user = request.user
        if id is None:
            return Response({'message': "You haven't provided an ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        post_obj = get_object_or_404(FoodPost, id=id)
        if post_obj.is_public ==False and post_obj.created_by !=user:
            return Response({'message': "sorry it`s private meal"}, status=status.HTTP_400_BAD_REQUEST)
        ser = FPost_serializer(post_obj, context={'request': request})
        return Response({'data': ser.data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        user = request.user

        post_ser = FPost_serializer(data=data, context={'request': request})
        post_ser.is_valid(raise_exception=True)
        post_ser.save(created_by=user)
        return Response({'data': post_ser.data}, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        id = kwargs.get("id")
        if id is None:
            return Response({'message': "You haven't provided an ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        post_obj = get_object_or_404(FoodPost, id=id)

        if post_obj.created_by != user:
            return Response({'message': "You do not have permission to edit this post"}, status=status.HTTP_403_FORBIDDEN)

        if 'images' in data:
            images = request.FILES.getlist('images')
            for image in images:
                ImagePost.objects.create(post=post_obj, image=image)
        
        post_ser = FPost_serializer(post_obj, data=data, partial=True, context={'request': request})
        post_ser.is_valid(raise_exception=True)
        post_ser.save()
        return Response({'post': post_ser.data, 'message': 'Post updated successfully'}, status=status.HTTP_202_ACCEPTED)
    
    def put(self,request,*args,**kwargs):
        data = request.data
        user= request.user

        id = kwargs.get("id",None)
        if id is None:
            return Response({'message': "You haven't provided an ID"}, status=status.HTTP_400_BAD_REQUEST)
        post_obj = get_object_or_404(FoodPost, id=id)
        com_ser = Comment_serializer(data=data)
        com_ser.is_valid(raise_exception=True)
        com_ser.save(post_obj=post_obj,commented_by=user)
        return Response({'comment': com_ser.data, 'message': 'comment uploaded successfully'}, status=status.HTTP_202_ACCEPTED)


        




class Profile_View(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        username = kwargs.get("username", None)
        if username:
            user_obj = get_object_or_404(User, username=username)
        else:
            user_obj = request.user
        
        user_ser = UserSerializer(user_obj)
        
        posts = FoodPost.objects.filter(created_by=user_obj, is_public=True) if username else FoodPost.objects.filter(created_by=user_obj)
        posts_ser = FPost_serializer(posts, many=True)
        advice = get_advice(user_obj)
        if user_obj.profile.account_type =='premium':
            diagram =get_daily_avg_ben_koef(user_obj)
            return Response({'data': user_ser.data, 'posts': posts_ser.data,'diagram':diagram ,'advice':advice }, status=status.HTTP_200_OK)
        return Response({'data': user_ser.data, 'posts': posts_ser.data,'advice':advice}, status=status.HTTP_200_OK)
    
    def patch(self, request):
        data = request.data
        user = request.user
        profile = Profile.objects.get(user=user)

        profile_ser = ProfileSerializer(profile, data=data, partial=True)
        if profile_ser.is_valid(raise_exception=True):
            profile_ser.save()
            return Response({'data': profile_ser.data}, status=status.HTTP_205_RESET_CONTENT)

class Settings_View(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user_obj = request.user
        data = request.data
        changes = 0

        if 'username' in data and data['username']:
            user_obj.username = data['username']
            changes = 1
        if 'email' in data and data['email']:
            user_obj.email = data['email']
            changes = 1

        if changes:
            user_obj.save()

        user_ser = UserSerializer(user_obj)
        return Response({'data': user_ser.data}, status=status.HTTP_202_ACCEPTED)

class Like_View(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        likes_query = Like.objects.filter(liked_by=user)
        likes_ser = Like_serializer(likes_query, many=True)
        return Response({'data': likes_ser.data}, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        user = request.user

        if id:
            post_obj = get_object_or_404(FoodPost, id=id)
            like_obj, created = Like.objects.get_or_create(post=post_obj, liked_by=user)

            if created:
                return Response({'data': Like_serializer(like_obj).data}, status=status.HTTP_201_CREATED)
            else:
                like_obj.delete()
                return Response({'message': 'Like removed'}, status=status.HTTP_204_NO_CONTENT)

class Posts_search(ListAPIView):
    queryset = FoodPost.objects.filter(is_public=True)

    serializer_class = FPost_serializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'composition','created_by','cat']

class Bookmark_View(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        bookmarks_query = Bookmark.objects.filter(marked_by=user)
        bookmarks_ser = Bookmark_serializer(bookmarks_query,many=True)
        return Response({'data':bookmarks_ser.data},status=status.HTTP_302_FOUND)

    def post(self,request,*args,**kwargs):
        user =request.user
        id = kwargs.get("id",None)
        if id is None:
            return Response({'message': "You haven't provided an ID"}, status=status.HTTP_400_BAD_REQUEST)
        post_obj = get_object_or_404(FoodPost, id=id)
        bookmark_obj = Bookmark.objects.create(marked_by=user,post=post_obj)
        bookmark_ser = Bookmark_serializer(bookmark_obj)
        return Response({'data':bookmark_ser.data},status=status.HTTP_302_FOUND)
        
