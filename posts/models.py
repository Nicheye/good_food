from django.db import models
from authentification.models import User
# Create your models here.



class FoodPost(models.Model):
    title = models.CharField(max_length=100)
    composition = models.TextField(max_length=500)
    weight = models.IntegerField(default=0)
    proteins = models.IntegerField(default=0, blank=True)
    fats = models.IntegerField(default=0, blank=True)
    carbohydrates = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    ben_koef= models.IntegerField(default=0)


class ImagePost(models.Model):
    post = models.ForeignKey(FoodPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')
