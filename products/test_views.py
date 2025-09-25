import pytest
import json
from decimal import Decimal
from django.test import Client
from django.urls import reverse
from products.models import Category, Product


@pytest.mark.django_db
class TestProductViews:
    def setup_method(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic devices"
        )

        self.product1 = Product.objects.create(
            name="Laptop",
            description="Gaming laptop",
            price=Decimal("999.99"),
            stock=10,
            category=self.category
        )

        self.product2 = Product.objects.create(
            name="Mouse",
            description="Wireless mouse",
            price=Decimal("25.99"),
            stock=5,
            category=self.category
        )

    def test_product_api_success(self):
        response = self.client.get(f'/api/products/{self.product1.id}/')

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['name'] == 'Laptop'
        assert data['price'] == '999.99'
        assert data['category'] == 'Electronics'

    def test_product_api_not_found(self):
        response = self.client.get('/api/products/999/')

        assert response.status_code == 404
        data = json.loads(response.content)
        assert data['error'] == 'Product not found'

    def test_category_products_count(self):
        response = self.client.get('/api/categories/count/')

        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data['categories']) == 1
        assert data['categories'][0]['category'] == 'Electronics'
        assert data['categories'][0]['product_count'] == 2