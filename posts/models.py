from django.db import models
from authentification.models import User

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
    ben_koef = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_posts')
    CAT_CHOICES = (
    ('похудение', 'Похудение'),
    ('спортпит', 'Спортивное питание'),
    ('веган', 'Веганы и Вегетарианцы'),
    ('здоровье', 'Полезно для здоровья'),
    ('анти-Эйджинг', 'Анти-Эйджинг'),
    ('семья', 'Семейное Питание'),
    ('мед', 'Питание при Медицинских Состояниях'),)

    cat = models.CharField(max_length=40, choices=CAT_CHOICES, default='здоровье')

    def __str__(self) -> str:
        return self.title + " " +str(self.id)

class ImagePost(models.Model):
    post = models.ForeignKey(FoodPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')

class Like(models.Model):
    post = models.ForeignKey(FoodPost, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
