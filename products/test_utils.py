import pytest
from decimal import Decimal
from django.utils import timezone
from products.models import Category, Product
from products.utils import ProductUtils, calculate_tax, format_currency, calculate_shipping_cost, InventoryManager


@pytest.mark.django_db
class TestProductUtils:
    def setup_method(self):
        self.category = Category.objects.create(name="Electronics")
        self.product1 = Product.objects.create(
            name="Laptop",
            price=Decimal("1000.00"),
            stock=10,
            category=self.category
        )
        self.product2 = Product.objects.create(
            name="Mouse",
            price=Decimal("50.00"),
            stock=5,
            category=self.category
        )

    def test_calculate_bulk_discount(self):
        products = [self.product1, self.product2]
        result = ProductUtils.calculate_bulk_discount(products, 10)

        assert result['original_total'] == Decimal('1050.00')
        assert result['discounted_total'] == Decimal('945.00')
        assert result['savings'] == Decimal('105.00')

    def test_get_low_stock_products(self):
        low_stock_products = ProductUtils.get_low_stock_products(threshold=8)
        assert len(low_stock_products) == 1
        assert low_stock_products[0] == self.product2


class TestUtilityFunctions:
    def test_calculate_tax(self):
        price = Decimal('100.00')
        taxed_price = calculate_tax(price, 0.1)
        assert taxed_price == Decimal('110.00')

    def test_format_currency(self):
        amount = Decimal('123.456')
        formatted = format_currency(amount)
        assert formatted == "$123.46"

    def test_calculate_shipping_cost(self):
        cost = calculate_shipping_cost(2.5, 500)
        assert isinstance(cost, Decimal)
        assert cost > Decimal('0')


@pytest.mark.django_db
class TestInventoryManager:
    def setup_method(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            price=Decimal("100.00"),
            stock=10,
            category=self.category
        )
        self.inventory = InventoryManager()

    def test_add_stock(self):
        initial_stock = self.product.stock
        self.inventory.add_stock(self.product, 5)

        self.product.refresh_from_db()
        assert self.product.stock == initial_stock + 5

        history = self.inventory.get_operation_history()
        assert len(history) == 1
        assert history[0]['type'] == 'add'