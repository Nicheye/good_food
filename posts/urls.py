

from django.urls import path
from .views import *
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'', Lenta_View.as_view())
router.register(r'post', Post_View.as_view())


urlpatterns = router.urls