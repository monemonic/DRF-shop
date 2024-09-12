from rest_framework import viewsets, status
from rest_framework.pagination import (
    LimitOffsetPagination, PageNumberPagination
)
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from shop.models import (
    Category,
    Product,
    ShoppingCart
)
from .serializers import (
    ShoppingCartSerializer,
    ProductReadSerializer,
    CategoryWithSubcategorySerializer,
    ShoppingCartUpdateSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryWithSubcategorySerializer
    pagination_class = LimitOffsetPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductReadSerializer
    pagination_class = PageNumberPagination

    @action(detail=True, methods=["POST", "PATCH"])
    def shopping_cart(self, request, pk):
        """Добавление и удаление продуктов из корзины."""

        if request.method == 'PATCH':
            product = get_object_or_404(ShoppingCart, product=pk).pk
            amount = request.data.get('amount')
            if amount:
                print('1')
                serializer = ShoppingCartUpdateSerializer(
                    data=(
                        {"amount": request.data["amount"], "product": product}
                    )
                )
                print(serializer)

            else:
                return Response(
                    "Вы не добавляли в корзину этот продукт.",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            product = get_object_or_404(Product, pk=pk).pk
            serializer = ShoppingCartSerializer(
                data=(
                    {"product": product,
                     "user": self.request.user.id,
                     })
            )
        print(3)
        serializer.is_valid(raise_exception=True)
        print(4)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
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
