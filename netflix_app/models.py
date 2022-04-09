from django.db import models
from django.core.validators import MaxValueValidator
from datetime import date

class Category(models.Model):
    type = models.CharField(max_length=64)
    
    class Meta:
        verbose_name_plural = 'categories' 

    def __str__(self):
        return f"CATEGORY: {self.type}"

class Genre(models.Model):
    type = models.CharField(max_length=64)
    tagline = models.CharField(max_length=255)

    def __str__(self):
        return f"GENRE: {self.type}"

class Product(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    genres = models.ManyToManyField(Genre, related_name="products")
    image_url = models.URLField(blank=True, null=True)
    year_released = models.DateField(validators=[MaxValueValidator(limit_value=date.today)])
    is_original = models.BooleanField(default=False, verbose_name="Netflix original")

    def get_average_rating(self):
        product_reviews = self.reviews
        # product_reviews = Review.objects.filter(product=self)
        if product_reviews.count() == 0:
            return None

        avg_rating_dict = product_reviews.aggregate(models.Avg("rating"))
        return round(list(avg_rating_dict.values())[0], 2)

    def __str__(self):
        return f"PRODUCT: {self.title}"

class Review(models.Model):
    class Rating(models.IntegerChoices):
        AWFUL = 1
        DECENT = 2
        AVERAGE = 3
        GOOD = 4
        AMAZING = 5
   
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=Rating.choices)
    username = models.CharField(max_length=64)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"REVIEW: {self.product.title} [{self.rating}]: {self.comment} --{self.username}"
