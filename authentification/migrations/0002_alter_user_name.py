# Generated by Django 4.2.6 on 2023-11-09 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]