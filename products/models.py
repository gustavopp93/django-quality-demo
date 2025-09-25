from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import datetime


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

    def apply_discount(self, discount_percentage):
        if discount_percentage < 0 or discount_percentage > 100:
            raise ValueError("Discount must be between 0 and 100")
        discount_amount = self.price * (Decimal(str(discount_percentage)) / 100)
        return self.price - discount_amount

    def get_status(self):
        if not self.is_active:
            return "Inactive"
        elif self.stock == 0:
            return "Out of Stock"
        elif self.stock < 10:
            return "Low Stock"
        else:
            return "In Stock"

    def get_legacy_data(self):
        data = {}
        data['name'] = self.name
        data['price'] = self.price
        data['stock'] = self.stock

        if self.category:
            data['category'] = self.category.name
        else:
            data['category'] = "No Category"

        today = datetime.datetime.now()

        if today.weekday() == 0:
            data['day'] = "Monday"
        elif today.weekday() == 1:
            data['day'] = "Tuesday"
        elif today.weekday() == 2:
            data['day'] = "Wednesday"
        elif today.weekday() == 3:
            data['day'] = "Thursday"
        elif today.weekday() == 4:
            data['day'] = "Friday"
        elif today.weekday() == 5:
            data['day'] = "Saturday"
        else:
            data['day'] = "Sunday"

        return data
