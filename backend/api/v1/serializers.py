from django.contrib.auth import get_user_model
from rest_framework import serializers

from shop.models import (
    Category,
    ImageProduct,
    Product,
    Subcategory,
    ShoppingCart
)


User = get_user_model()


class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = ("id", "category", "name", "picture")


class CategoryWithSubcategorySerializer(serializers.ModelSerializer):
    subcategory = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "picture", "subcategory")

    def get_subcategory(self, obj):
        return SubcategorySerializer(
            Subcategory.objects.filter(category=obj),
            many=True,
            read_only=True
        ).data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("id", "name", "picture")


class ImageProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageProduct
        fields = ("image",)


class ProductReadSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField(read_only=True)
    subcategory = SubcategorySerializer()
    category = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "name", "slug", "subcategory", "category", "price", "picture"
        )

    def get_picture(self, obj):
        return ImageProductSerializer(
            ImageProduct.objects.filter(product=obj.id),
            many=True,
            read_only=True
        ).data

    def get_category(self, obj):
        return CategorySerializer(obj.subcategory.category).data


class ShoppingCartUpdateSerializer(serializers.ModelSerializer):
    amount = serializers.CharField()

    class Meta:
        model = ShoppingCart
        fields = ('amount',)

    def validate_amount(self, value):
        if value.isdigit():
            return int(value)
        elif value in ["+", "-"]:
            return value
        raise serializers.ValidationError("Неверный формат для поля amount. Ожидается число, '+' или '-'.")


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ("user", "product", "amount", "price")

    def get_price(self, obj):
        return obj.product.price*obj.amount
