from django.urls import path
from .views import *

urlpatterns = [
    path("categories/", category_list_view, name="category-list"),
    path("categories/<int:category_id>/", category_detail_view, name="category-detail"),

    path("genres/", genre_list_view, name="genre-list"),
    path("genres/<int:genre_id>/", genre_detail_view, name="genre-detail"),

    path("products/", product_list_view, name="product-list"),
    path("products/<int:product_id>/", product_detail_view, name="product-detail"),

    path("reviews/", review_list_view, name="review-list"),
    path("reviews/<int:review_id>/", review_detail_view, name="review-detail"),
]