from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet


router_v_1 = DefaultRouter()
router_v_1.register("products", ProductViewSet, basename="products")
router_v_1.register("categories", CategoryViewSet, basename="categories")


urlpatterns = [
    path("", include(router_v_1.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
