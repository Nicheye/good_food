# Generated by Django 4.2.6 on 2024-05-26 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_foodpost_cat_foodpost_is_public_like_foodpost_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodpost',
            name='cat',
            field=models.CharField(choices=[('похудение', 'Похудение'), ('спортпит', 'Спортивное питание'), ('веган', 'Веганы и Вегетарианцы'), ('здоровье', 'Полезно для здоровья'), ('анти-Эйджинг', 'Анти-Эйджинг'), ('семья', 'Семейное Питание'), ('мед', 'Питание при Медицинских Состояниях')], default='здоровье', max_length=40),
        ),
    ]
