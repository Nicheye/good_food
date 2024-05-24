# Generated by Django 4.2.6 on 2024-05-24 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0004_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=10)),
                ('account_type', models.CharField(choices=[('free', 'Free'), ('premium', 'Premium')], default='free', max_length=10)),
                ('weight', models.IntegerField(default=0)),
                ('avatar', models.ImageField(upload_to='avatars')),
                ('bio', models.CharField(blank=True, max_length=1000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
