from django.urls import include, path
from rest_framework.routers import SimpleRouter

from deals.views import DealViewSet

router = SimpleRouter()
router.register('deals', DealViewSet, basename='deals')

urlpatterns = [
    path('', include(router.urls)),
]
