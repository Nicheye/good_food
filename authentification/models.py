from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class User(AbstractUser):
	username = models.CharField(max_length=255,unique=True)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []
	def profile(self):
		profile = Profile.objects.get(user=self)

class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	ACCOUNT_CHOICES = (
        ('free', 'Free'),
        ('premium', 'Premium'),
    )
	SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
	sex = models.CharField(max_length=10, choices=SEX_CHOICES, default='M')
	account_type = models.CharField(max_length=10, choices=ACCOUNT_CHOICES, default='free')
	weight = models.IntegerField(default=0)
	avatar = models.ImageField(upload_to="avatars")
	bio = models.CharField(max_length=1000,blank=True)

	def create_user_profile(sender,instance,created,**kwargs):
		if created:
			Profile.objects.create(user=instance)
	def save_user_profile(sender,instance,**kwargs):
		instance.profile.save()
	
	post_save.connect(create_user_profile,sender=User)
	post_save.connect(save_user_profile,sender=User)