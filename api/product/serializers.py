from product.models import Category
from rest_framework.serializers import ModelSerializer


class CategorySerializers(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
