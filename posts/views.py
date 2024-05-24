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
class Lenta_View(ListAPIView):
    serializer_class = FPost_serializer
    queryset = FoodPost.objects.order_by('-created_at')


class Post_View(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data = request.data
        user = request.user

        post_ser = FPost_serializer(data=data)
        if post_ser.is_valid(raise_exception=True):
            post_ser.save(created_by=user)
            return Response({'post':post_ser.data},status=status.HTTP_201_CREATED)
    
    def patch(self,request,*args,**kwargs):
        data = request.data
        user = request.user

        id = kwargs.get("id")
        if id is not None:
            post_obj = get_object_or_404(FoodPost,id=id)
            if post_obj:
                images = request.data['images']
                for image in images:
                    new_obj= ImagePost.objects.create(post=post_obj,image=image)
                    new_obj.save()
                post_obj.ben_koef = calculate_usefulness(post_obj)
                post_obj.save()
                post_ser = FPost_serializer(post_obj)

                return Response({'post':post_ser.data,'message':'new photoes successfully added'},status=status.HTTP_202_ACCEPTED)
        return Response({'message':"you havent provided id"})



