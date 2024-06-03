from collections import Counter
from .models import Like,FoodPost,UsefulnessHistory
from django.db.models import Q, Count
from django.db.models import Avg
from django.db.models.functions import TruncDay
from .serializers import FPost_serializer,UsefulnessHistorySerializer
import requests




def get_favorite_category(user):
    liked_posts = Like.objects.filter(liked_by=user)
    categories = [post.post.cat for post in liked_posts]
    favorite_category = Counter(categories).most_common(1)[0][0] if categories else None
    return favorite_category

def recommended_posts(user):
    fav_cat = get_favorite_category(user)
    firstly = FoodPost.objects.filter(cat=fav_cat, is_public=True) if fav_cat else FoodPost.objects.none()

    if user.profile.goal == 'Сушка':
        query = Q(cat='похудение') | Q(cat="спортпит")
    elif user.profile.goal == 'Баланс':
        query = Q(cat='здоровье') | Q(cat="анти-Эйджинг")
    elif user.profile.goal == 'Похудение':
        query = Q(cat='похудение') | Q(cat="веган")
    elif user.profile.goal == 'Набор':
        query = Q(cat='спортпит') | Q(cat="здоровье")
    else:
        secondly = FoodPost.objects.annotate(like_count=Count('likes')).order_by('-like_count')
        thirdly = FoodPost.objects.filter(cat='здоровье', is_public=True)
        return (firstly | secondly | thirdly).distinct()

    secondly = FoodPost.objects.filter(query, is_public=True)
    thirdly = FoodPost.objects.filter(cat='здоровье', is_public=True)

    final = (firstly | secondly | thirdly).distinct().annotate(like_count=Count('likes')).order_by('-like_count')
    return final

def most_popular():
    query = Q(cat='спортпит') | Q(cat="здоровье")
    posts_query = FoodPost.objects.filter(query).annotate(like_count=Count('likes')).order_by('-like_count')
    if posts_query.count() < 1:
        posts_query = FoodPost.objects.all().annotate(like_count=Count('likes')).order_by('-like_count')
    return posts_query
    
def get_daily_avg_ben_koef(user):
    # Group by the date and calculate the average ben_koef using UsefulnessHistory
    daily_avg = (
        UsefulnessHistory.objects
        .filter(food_post__created_by=user)  # Filter by posts created by the user
        .annotate(day=TruncDay('calculated_at'))  # Truncate calculated_at to day
        .values('day')  # Group by day
        .annotate(avg_ben_koef=Avg('usefulness_score'))  # Calculate the average usefulness score for each day
        .order_by('day')  # Order by day
    )
    
    # Serialize the result
    daily_ser = UsefulnessHistorySerializer(daily_avg, many=True)
    return daily_ser.data


def get_advice(user):
    pass


