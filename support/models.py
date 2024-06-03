from django.db import models
from posts.models import FoodPost
from authentification.models import User
class Report(models.Model):
    post =models.ForeignKey(FoodPost,on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField(default="descr")
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
    ('approved',"Approved"),
    ('pending',"Pending"),
    ('declined',"declined"))
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='pending')
    message = models.CharField(max_length=500,blank=True)


class Ticket(models.Model):
    reason = models.CharField(max_length=120)
    description = models.TextField()

    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = (
    ('approved',"Approved"),
    ('pending',"Pending"),
    ('declined',"declined"))
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='pending')
    respond = models.CharField(max_length=1000,blank=True)
