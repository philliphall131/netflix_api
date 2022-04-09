# built in serializer, for internal data use primarily
# from django.core import serializers
# data = serializers.serialize("json", Category.objects.all())

class SerializerBase:    
    def serialize_all(self, item_list):
        serialized_data = []
        for item in item_list:
            serialized_data.append(self.serialize(item))
        return serialized_data


## Category serializers

class CategorySerializer(SerializerBase):
    def serialize(self, category):
        return {
            "id": category.id,
            "type": category.type,
            "products": self.serialize_products(category.products.all())
        }
    
    @staticmethod
    def serialize_products(products):
        return [p.id for p in products]

class CategoryNestedSerializer(CategorySerializer):
    @staticmethod
    def serialize_products(products):
        return ProductSerializer().serialize_all(products)


## Genre serializers

class GenreSerializer(SerializerBase):
    def serialize(self, genre):
        return {
            "id": genre.id,
            "type": genre.type,
            "tagline": genre.tagline,
            "products": self.serialize_products(genre.products.all())
        }

    @staticmethod
    def serialize_products(products):
        return [ p.id for p in products ]

class GenreNestedSerializer(GenreSerializer):
    @staticmethod
    def serialize_products(products):
        return ProductSerializer().serialize_all(products)


## Product serializers

class ProductSerializer(SerializerBase):
    def serialize(self, product):
        return {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "category": self.serialize_category(product.category),
            "genres": self.serialize_genres(product.genres.all()),
            "image_url": product.image_url,
            "year_released": product.year_released,
            "is_original": product.is_original,
            "average_rating": product.get_average_rating(),
            "reviews": self.serialize_reviews(product.reviews.all())
        }

    @staticmethod
    def serialize_category(category):
        return category.id

    @staticmethod
    def serialize_genres(genres):
        return [ g.id for g in genres ]

    @staticmethod
    def serialize_reviews(reviews):
        return [ r.id for r in reviews ]

class ProductNestedSerializer(ProductSerializer):
    @staticmethod
    def serialize_category(category):
        return CategorySerializer().serialize(category)

    @staticmethod
    def serialize_products(genres):
        return GenreSerializer().serialize_all(genres)

    @staticmethod
    def serialize_reviews(reviews):
        return ReviewSerializer().serialize_all(reviews)


## Review serializers

class ReviewSerializer(SerializerBase):
    def serialize(self, review):
        return {
            "id": review.id,
            "product": self.serialize_product(review.product),
            "rating": review.rating,
            "username": review.username,
            "comment": review.comment or "This user did not provide a comment."
        }

    @staticmethod
    def serialize_product(product):
        return product.id

class ReviewNestedSerializer(ReviewSerializer):
    @staticmethod
    def serialize_product(product):
        return ProductSerializer().serialize(product)