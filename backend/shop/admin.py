from django.contrib import admin

from .models import Category, ImageProduct, Product, Subcategory


class ImageProductInline(admin.StackedInline):
    """Добавление изображений продукта."""

    model = ImageProduct
    extra = 1
    max_num = 3


class ProductAdmin(admin.ModelAdmin):
    """Добавление, удаление, изменений продуктов."""
    inlines = (ImageProductInline,)
    list_display = (
        "name",
        "slug",
        "price",
        "subcategory",
    )

    search_fields = ("name",)
    list_filter = ("subcategory__name",)
    list_display_links = ("name",)


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subcategory)
