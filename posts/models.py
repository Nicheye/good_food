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
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    ben_koef= models.IntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    CAT_CHOICES = (
        
		
		('Похудение', 'похудение'),
        ('Спортивное питание', 'спортпит'),
        ('Веганы и Вегетарианцы', 'веган'),
        ('Полезно для здоровья', 'здоровье'),
        ('Анти-Эйджинг', 'анти-Эйджинг'),
        ('Семейное Питание', 'семья'),
        ('Питание при Медицинских Состояниях', 'мед'),
    )
    cat = models.CharField(max_length=40,choices=CAT_CHOICES,default='здоровье')

class ImagePost(models.Model):
    post = models.ForeignKey(FoodPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')

class Like(models.Model):
    post = models.ForeignKey(FoodPost,on_delete=models.CASCADE)
    liked_by= models.ForeignKey(User,on_delete=models.CASCADE)

