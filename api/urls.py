from django.urls import path
from api.product.views import CategoryAPI
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('category-api', CategoryAPI)

urlpatterns = [
]

urlpatterns += router.urls
