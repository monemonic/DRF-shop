from django.contrib import admin

from .models import Category, Product, Subcategory, ImageProduct


class ImageProductInline(admin.StackedInline):
    model = ImageProduct
    extra = 1
    max_num = 3


class ProductAdmin(admin.ModelAdmin):
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
