from django.urls import path
from .views import Lenta_View, Post_View, Profile_View, Settings_View, Like_View, Posts_search, Bookmark_View, Separated_lenta

urlpatterns = [
    path('posts/', Post_View.as_view(), name='post_list_create'),  
    path('posts/<int:id>/', Post_View.as_view(), name='post_detail'), 
    path('', Lenta_View.as_view(), name='lenta'),
    path('<slug:filter>/', Separated_lenta.as_view(), name='lenta'),
    
    path('profile/', Profile_View.as_view(), name='profile_mine'),
    path('profile/<slug:username>/', Profile_View.as_view(), name='profile_other'),
    path('settings/', Settings_View.as_view(), name='settings'),
    path('like/', Like_View.as_view(), name='like_all'),
    path('like/<int:id>/', Like_View.as_view(), name='like_add'),
    path('search', Posts_search.as_view(), name='search'),
    path('bookmarks/', Bookmark_View.as_view(), name='bookmark_list'),
    path('bookmarks/<int:id>/', Bookmark_View.as_view(), name='bookmark_add'),
]
