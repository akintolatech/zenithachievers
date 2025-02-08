from django.db import models
from django.contrib.auth.models import User

class Product (models.Model):
    name = models.CharField(max_length=50, unique=True)  # Now dynamic
    product_image = models.ImageField(upload_to="products", null=False)

    def __str__(self):
        return self.name
