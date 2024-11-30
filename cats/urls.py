from django.urls import path, include
from rest_framework import routers
from cats.views import CatViewSet, MissionViewSet

app_name = 'restaurant'

router = routers.DefaultRouter()
router.register('cats', CatViewSet)
router.register('missions', MissionViewSet)

urlpatterns = [path('', include(router.urls))]
