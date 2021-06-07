from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializers
from product.models import Category


class CategoryAPI(ModelViewSet):

    serializer_class = CategorySerializers
    queryset = Category.objects.all()
