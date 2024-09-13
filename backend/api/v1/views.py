from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import (
    LimitOffsetPagination, PageNumberPagination
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    CategoryWithSubcategorySerializer,
    ProductReadSerializer,
    ShoppingCartAllProductsSerializer,
    ShoppingCartSerializer,
    ShoppingCartUpdateSerializer,
)
from backend.constants import (
    CHANGE_VALUE_SHOPPING_CART,
    VALUE_FOR_REMOVING_PRODUCT
)
from shop.models import (
    Category,
    Product,
    ShoppingCart,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API для отображения категорий с подкатегориями."""

    queryset = Category.objects.all()
    serializer_class = CategoryWithSubcategorySerializer
    pagination_class = LimitOffsetPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """API для продуктов и обработки корзины."""

    queryset = Product.objects.all()
    serializer_class = ProductReadSerializer
    pagination_class = PageNumberPagination

    @action(detail=True, methods=["POST", "PATCH"])
    def add_shopping_cart(self, request, pk):
        """Добавление, изменение количества и удаление продуктов из корзины."""
        if request.method == 'PATCH':
            serializer = ShoppingCartUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            amount = serializer.validated_data.get("amount")
            product = get_object_or_404(ShoppingCart, product=pk)
            if amount == '+':
                product.amount += CHANGE_VALUE_SHOPPING_CART
            elif amount == '-':
                product.amount -= CHANGE_VALUE_SHOPPING_CART
            else:
                product.amount = amount
            if product.amount == VALUE_FOR_REMOVING_PRODUCT:
                product.delete()
                return Response(
                    "Продукт успешно удален из корзины",
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                product.save()
                serializer = ShoppingCartSerializer(product)

        else:
            product = get_object_or_404(Product, pk=pk).pk
            serializer = ShoppingCartSerializer(
                data=(
                    {"product": product,
                     "user": self.request.user.id,
                     }), context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @add_shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = self.request.user
        product = get_object_or_404(Product, pk=pk)
        count_del_objects, _ = ShoppingCart.objects.filter(
            user=user, product=product
        ).delete()

        if not count_del_objects:
            return Response(
                "Вы не добавляли в корзину этот продукт.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            "Продукт успешно удален из корзины",
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=["DELETE"])
    def clean_all_shopping_cart(self, request):
        """Удаление всех продуктов из корзины пользователя."""
        count_del_objects, _ = ShoppingCart.objects.filter(
            user=self.request.user,
        ).delete()

        if not count_del_objects:
            return Response(
                "Корзина пуста.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            "Корзина успешно очищена.",
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=["GET"],
            permission_classes=(IsAuthenticated,)
            )
    def shopping_cart(self, request):
        """
        Отображение всех продуктов и их общей
        цены в корзине пользователя.
        """
        queryset = ShoppingCart.objects.filter(user=self.request.user)
        count_products = len(queryset)
        total_price = sum([i.product.price*i.amount for i in queryset])
        serializer = ShoppingCartAllProductsSerializer(
            queryset,
            context={'count': count_products, "total_price": total_price}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
