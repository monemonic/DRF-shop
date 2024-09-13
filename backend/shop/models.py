from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from backend.constants import (
    CATEGORY_NAME_MAX_LENGTH,
    MAX_VALUE_VALIDATOR_AMOUNT,
    MAX_VALUE_VALIDATOR_PRICE,
    MIN_VALUE_VALIDATOR_AMOUNT,
    MIN_VALUE_VALIDATOR_PRICE,
    PRODUCT_NAME_FIELD_MAX_LENGTH,
    PRODUCT_SLUG_FIELD_MAX_LENGTH,
    TAG_CATEGORY_FIELD_MAX_LENGTH,
)


User = get_user_model()


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(
        "Название",
        max_length=CATEGORY_NAME_MAX_LENGTH,
        help_text=f"Название категории, не более \
            {CATEGORY_NAME_MAX_LENGTH} символов",
    )
    slug = models.SlugField(
        "Слаг",
        unique=True,
        max_length=TAG_CATEGORY_FIELD_MAX_LENGTH,
        help_text=f"Слаг категории, не более \
            {TAG_CATEGORY_FIELD_MAX_LENGTH} символов",
    )
    picture = models.ImageField(
        upload_to="backend/categories/",
        verbose_name="Изображение",
        help_text="Изображение категории",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "категории"


class Subcategory(models.Model):
    """Модель подкатегории."""

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Подкатегория",
        help_text="К какой категории относится данная подкатегория",
    )
    name = models.CharField(
        "Название",
        max_length=CATEGORY_NAME_MAX_LENGTH,
        help_text=f"Название подкатегории, не более \
            {CATEGORY_NAME_MAX_LENGTH} символов",
    )
    slug = models.SlugField(
        "Слаг",
        unique=True,
        max_length=TAG_CATEGORY_FIELD_MAX_LENGTH,
        help_text=f"Слаг подкатегории, не более \
            {TAG_CATEGORY_FIELD_MAX_LENGTH} символов",
    )
    picture = models.ImageField(
        upload_to="backend/categories/",
        verbose_name="Изображение",
        help_text="Изображение подкатегории",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "подкатегории"


class Product(models.Model):
    """Модель продукта."""

    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        verbose_name="Подкатегория продукта",
        help_text="К какой подкатегории относится продукт",
    )
    name = models.CharField(
        "Название",
        max_length=PRODUCT_NAME_FIELD_MAX_LENGTH,
        help_text=f"Название продукта, не более \
            {PRODUCT_NAME_FIELD_MAX_LENGTH} символов",
    )
    slug = models.SlugField(
        "Слаг",
        unique=True,
        max_length=PRODUCT_SLUG_FIELD_MAX_LENGTH,
        help_text=f"Слаг продукта, не более \
            {PRODUCT_SLUG_FIELD_MAX_LENGTH} символов",
    )
    price = models.PositiveIntegerField(
        "Цена",
        help_text="Цена продукта",
        validators=[
            MinValueValidator(
                MIN_VALUE_VALIDATOR_PRICE,
                message=f"Значение не может быть меньше, \
                    чем {MIN_VALUE_VALIDATOR_PRICE}",
            ),
            MaxValueValidator(
                MAX_VALUE_VALIDATOR_PRICE,
                message=f"Значение не может быть больше, \
                    чем {MAX_VALUE_VALIDATOR_PRICE}",
            ),
        ],
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "продукты"


class ImageProduct(models.Model):
    """Модель изображений связанных с продуктами."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    image = models.ImageField(
        upload_to="backend/products/",
        verbose_name="Изображение",
        help_text="Изображение продукта",
    )

    def __str__(self):
        return f'id {self.product.id}, {self.product.name} изображение'

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "изображения продукта"


class ShoppingCart(models.Model):
    """Модель корзины."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, который добавил продукт.",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт",
        help_text="Продукт, добавленный пользователем.",
    )
    amount = models.PositiveSmallIntegerField(
        "Количество",
        help_text="Количество продуктов",
        validators=[
            MinValueValidator(
                MIN_VALUE_VALIDATOR_AMOUNT,
                message=f"Значение не может быть меньше, \
                    чем {MIN_VALUE_VALIDATOR_AMOUNT}",
            ),
            MaxValueValidator(
                MAX_VALUE_VALIDATOR_AMOUNT,
                message=f"Значение не может быть больше, \
                    чем {MIN_VALUE_VALIDATOR_AMOUNT}",
            ),
        ],
        default=1,
    )
