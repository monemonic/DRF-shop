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
    product = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('amount', "product")

    def validate_amount(self, value):
        print(type(value), value)
        if value.isdigit():
            print('odin')
            return int(value)
        elif value == '+':
            print('dva')
            return 1
        elif value == '-':
            return -1
        print('tri')
        raise serializers.ValidationError("Неверный формат для поля amount. Ожидается число, '+' или '-'.")

    def update(self, instance, validated_data):
        print("puk")
        amount = validated_data.get('amount')

        if isinstance(amount, int):
            instance.amount += amount
        elif amount == '+':
            instance.amount += 1
        elif amount == '-':
            instance.amount = max(1, instance.amount - 1)
        print(instance)
        print(validated_data)
        instance.save()
        return super().update(instance, validated_data)


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ("user", "product", "amount", "price")

    def get_price(self, obj):
        return obj.product.price*obj.amount
