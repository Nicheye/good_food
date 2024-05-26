from django.urls import path
from .views import Lenta_View, Post_View, Profile_View, Settings_View, Like_View

urlpatterns = [
    path('', Lenta_View.as_view(), name='lenta'),
    path('post/', Post_View.as_view(), name='post_list'),
    path('post/<int:id>', Post_View.as_view(), name='post_detail'),
    path('profile/', Profile_View.as_view(), name='profile_mine'),
    path('profile/<slug:username>', Profile_View.as_view(), name='profile_other'),
    path('settings/', Settings_View.as_view(), name='settings'),
    path('like/', Like_View.as_view(), name='like_all'),
    path('like/<int:id>', Like_View.as_view(), name='like_add'),
]
