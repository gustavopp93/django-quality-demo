import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from products.models import Category, Product


@pytest.mark.django_db
class TestCategoryModel:
    def test_category_creation(self):
        category = Category.objects.create(
            name="Electronics",
            description="Electronic devices and accessories"
        )
        assert str(category) == "Electronics"
        assert category.name == "Electronics"

    def test_category_without_description(self):
        category = Category.objects.create(name="Books")
        assert category.description == ""


@pytest.mark.django_db
class TestProductModel:
    def test_product_creation(self):
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(
            name="Laptop",
            description="Gaming laptop",
            price=Decimal("999.99"),
            stock=10,
            category=category
        )

        assert str(product) == "Laptop"
        assert product.price == Decimal("999.99")
        assert product.is_active is True

    def test_is_in_stock_method(self):
        category = Category.objects.create(name="Electronics")

        product_in_stock = Product.objects.create(
            name="Mouse",
            price=Decimal("25.00"),
            stock=5,
            category=category
        )

        product_out_of_stock = Product.objects.create(
            name="Keyboard",
            price=Decimal("50.00"),
            stock=0,
            category=category
        )

        assert product_in_stock.is_in_stock() is True
        assert product_out_of_stock.is_in_stock() is False

    def test_apply_discount_method(self):
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(
            name="Phone",
            price=Decimal("100.00"),
            stock=5,
            category=category
        )

        discounted_price = product.apply_discount(20)
        assert discounted_price == Decimal("80.00")

    def test_apply_discount_invalid_percentage(self):
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(
            name="Phone",
            price=Decimal("100.00"),
            stock=5,
            category=category
        )

        with pytest.raises(ValueError):
            product.apply_discount(-10)

        with pytest.raises(ValueError):
            product.apply_discount(110)

    def test_get_status_method(self):
        category = Category.objects.create(name="Electronics")

        inactive_product = Product.objects.create(
            name="Old Phone",
            price=Decimal("50.00"),
            stock=20,
            category=category,
            is_active=False
        )

        out_of_stock_product = Product.objects.create(
            name="Sold Out Item",
            price=Decimal("100.00"),
            stock=0,
            category=category
        )

        low_stock_product = Product.objects.create(
            name="Limited Item",
            price=Decimal("200.00"),
            stock=5,
            category=category
        )

        in_stock_product = Product.objects.create(
            name="Available Item",
            price=Decimal("150.00"),
            stock=50,
            category=category
        )

        assert inactive_product.get_status() == "Inactive"
        assert out_of_stock_product.get_status() == "Out of Stock"
        assert low_stock_product.get_status() == "Low Stock"
        assert in_stock_product.get_status() == "In Stock"