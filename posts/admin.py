from django.contrib import admin


from .models import *

admin.site.register(FoodPost)
admin.site.register(ImagePost)
admin.site.register(Like)
admin.site.register(UserPreferences)
admin.site.register(UsefulnessHistory)
admin.site.register(Comment)
admin.site.register(Bookmark)
