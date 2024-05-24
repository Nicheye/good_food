
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *
urlpatterns = [
     
	path('logout/', LogoutView.as_view(), name ='logout'),
      path('register/',RegisterView.as_view()),
]