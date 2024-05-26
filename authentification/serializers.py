import os
from dotenv import load_dotenv

load_dotenv()
from rest_framework import serializers
from .models import User,Profile
from django.shortcuts import get_object_or_404
host = os.getenv('host')
class UserSerializer(serializers.ModelSerializer):
	profile = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields =['id','username','password','profile']
		extra_kwargs = {
			'password':{'write_only':True}
		}

	def create(self,validated_data):
		password = validated_data.pop('password',None)
		instance =  self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance
	def get_profile(self,obj):
		prof_obj = get_object_or_404(Profile,user=obj)
		if prof_obj:
			prof_ser = ProfileSerializer(prof_obj)
			return prof_ser.data


class ProfileSerializer(serializers.ModelSerializer):
	avatar = serializers.SerializerMethodField()
	class Meta:
		model = Profile
		fields =['sex','account_type','weight','height','age','avatar','bio']
	def get_avatar(self,obj):
		return host +str(obj.avatar.url)

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.RegexField(
        regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        write_only=True,
        error_messages={'invalid': ('Password must be at least 8 characters long with at least one capital letter and symbol')})
	
        
