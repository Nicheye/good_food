
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *
urlpatterns = [
     
	path('logout/', LogoutView.as_view(), name ='logout'),
    path('register/',RegisterView.as_view()),
    path('api/password-reset/request/', RequestPasswordReset.as_view(), name='password_reset_request'),
    path('api/password-reset/reset/<str:token>/', ResetPassword.as_view(), name='password_reset'),

]
