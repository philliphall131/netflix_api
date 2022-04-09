from django.forms import modelform_factory
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from .views_helpers import *


## Category view handlers

CategoryForm = modelform_factory(Category, fields="__all__") # Model Form class

@csrf_exempt
def category_list_view(request):
    if request.method != "GET": # don't allow CUD'ing for categories
        return bad_request() 
    return list_view(request, Category, CategoryForm, CategoryNestedSerializer)

@csrf_exempt
def category_detail_view(request, category_id):
    if request.method != "GET": # don't allow CUD'ing for categories
        return bad_request()
    return detail_view(request, Category, CategoryForm, CategoryNestedSerializer, category_id)


## Genre view handlers

GenreForm = modelform_factory(Genre, fields="__all__")

@csrf_exempt
def genre_list_view(request):
    if request.method != "GET": # don't allow CUD'ing for genres
        return bad_request() 
    return list_view(request, Genre, GenreForm, GenreNestedSerializer)

@csrf_exempt
def genre_detail_view(request, genre_id):
    if request.method != "GET": # don't allow CUD'ing for genres
        return bad_request()
    return detail_view(request, Genre, GenreForm, GenreNestedSerializer, genre_id)


## Product view handlers

ProductForm = modelform_factory(Product, fields="__all__")

@csrf_exempt
def product_list_view(request):
    return list_view(request, Product, ProductForm, ProductNestedSerializer)

@csrf_exempt
def product_detail_view(request, product_id):
    return detail_view(request, Product, ProductForm, ProductNestedSerializer, product_id)


## Review view handlers

ReviewForm = modelform_factory(Review, fields="__all__")

@csrf_exempt
def review_list_view(request):
    return list_view(request, Review, ReviewForm, ReviewNestedSerializer)

@csrf_exempt
def review_detail_view(request, review_id):
    disabled_fields_for_update = ["product", "username"] # prevent updating these fields
    return detail_view(request, Review, ReviewForm, ReviewNestedSerializer, review_id, disabled_fields_for_update)