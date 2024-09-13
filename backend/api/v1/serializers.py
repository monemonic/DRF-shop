from django.contrib.auth import get_user_model
from rest_framework import serializers

from shop.models import (
    Category,
    ImageProduct,
    Product,
    ShoppingCart,
    Subcategory
)


User = get_user_model()


class SubcategorySerializer(serializers.ModelSerializer):
    """Отображение подкатегорий."""

    class Meta:
        model = Subcategory
        fields = ("id", "category", "name", "picture")


class CategoryWithSubcategorySerializer(serializers.ModelSerializer):
    """Отображение категорий с их подкатегориями."""

    subcategory = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "picture", "subcategory")

    def get_subcategory(self, obj):
        return SubcategorySerializer(
            Subcategory.objects.filter(category=obj), many=True, read_only=True
        ).data


class CategorySerializer(serializers.ModelSerializer):
    """Отображение категорий."""

    class Meta:
        model = Category
        fields = ("id", "name", "picture")


class ImageProductSerializer(serializers.ModelSerializer):
    """Отображение изображений продуктов."""

    class Meta:
        model = ImageProduct
        fields = ("image",)


class ProductReadSerializer(serializers.ModelSerializer):
    """Отображение продуктов."""

    picture = serializers.SerializerMethodField(read_only=True)
    subcategory = SubcategorySerializer()
    category = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ("name", "slug", "subcategory",
                  "category", "price", "picture"
                  )

    def get_picture(self, obj):
        return ImageProductSerializer(
            ImageProduct.objects.filter(product=obj.id),
            many=True, read_only=True
        ).data

    def get_category(self, obj):
        return CategorySerializer(obj.subcategory.category).data


class ShoppingCartUpdateSerializer(serializers.ModelSerializer):
    """Изменение количества продуктов в корзине."""

    amount = serializers.CharField()

    class Meta:
        model = ShoppingCart
        fields = ("amount",)

    def validate_amount(self, value):
        if value.isdigit():
            return int(value)
        elif value in ["+", "-"]:
            return value
        raise serializers.ValidationError(
            "Неверный формат для поля amount. Ожидается число, '+' или '-'."
        )


class ShoppingCartReadSerializer(serializers.ModelSerializer):
    """Ответ API для продуктов в корзине."""

    product = ProductReadSerializer(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ("product", "amount", "price")

    def get_price(self, obj):
        return obj.product.price * obj.amount


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Создание и удаление продуктов из корзины."""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ShoppingCart
        fields = ("user", "product", "amount")

    def validate(self, data):
        user = self.context.get("request").user.id

        if ShoppingCart.objects.filter(
            user=user, product=data["product"]
        ).exists():
            raise serializers.ValidationError(
                {"product": "Нельза добавлять в "
                 "корзину одинаковые продукты."
                 }
            )
        return data

    def to_representation(self, instance):
        return ShoppingCartReadSerializer(instance).data


class ShoppingCartAllProductsSerializer(serializers.Serializer):
    """Отображение всех продуктов в корзине."""

    products = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField(read_only=True)
    count = serializers.SerializerMethodField()

    class Meta:
        fields = ("products", "count", "total_price")

    def get_products(self, obj):
        """Получение списка всех продуктов в корзине"""
        return ShoppingCartSerializer(
            obj, context=self.context, many=True
        ).data

    def get_count(self, obj):
        """Получение количества продуктов в корзине."""
        return self.context.get("count")

    def get_total_price(self, obj):
        """Получение общей стоимость продуктов в корзине."""
        return self.context.get("total_price")
