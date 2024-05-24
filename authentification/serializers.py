import os
from dotenv import load_dotenv

load_dotenv()
from rest_framework import serializers
from .models import User,Profile
host = os.getenv('host')
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields =['id','username','password']
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


class ProfileSerializer(serializers.ModelSerializer):
	avatar = serializers.SerializerMethodField()
	class Meta:
		model = Profile
		fields =['sex','account_type','weight','avatar','bio']
	def get_avatar(self,obj):
		return host +str(obj.avatar.url)

