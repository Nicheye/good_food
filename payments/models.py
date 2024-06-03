from django.db import models
from authentification.models import User
# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = (
    ('approved',"Approved"),
    ('pending',"Pending"),
    ('declined',"declined"))


    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='pending')
    
