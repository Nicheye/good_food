from django.contrib import admin


from .models import *

admin.site.register(FoodPost)
admin.site.register(ImagePost)
admin.site.register(Like)

