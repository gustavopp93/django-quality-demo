from decimal import Decimal
from django.utils import timezone
from datetime import timedelta


class ProductUtils:
    @staticmethod
    def calculate_bulk_discount(products, discount_percentage):
        if discount_percentage < 0 or discount_percentage > 100:
            raise ValueError("Invalid discount percentage")

        total_original = sum(p.price for p in products)
        total_discounted = sum(p.apply_discount(discount_percentage) for p in products)

        return {
            'original_total': total_original,
            'discounted_total': total_discounted,
            'savings': total_original - total_discounted
        }

    @staticmethod
    def get_low_stock_products(threshold=10):
        from .models import Product
        return Product.objects.filter(
            stock__lte=threshold,
            is_active=True
        ).select_related('category')

    @staticmethod
    def get_recent_products(days=30):
        from .models import Product
        cutoff_date = timezone.now() - timedelta(days=days)
        return Product.objects.filter(
            created_at__gte=cutoff_date,
            is_active=True
        ).order_by('-created_at')


def calculate_tax(price, tax_rate=0.1):
    if tax_rate < 0:
        return price
    return price * (1 + Decimal(str(tax_rate)))


def format_currency(amount):
    return f"${amount:.2f}"


def calculate_shipping_cost(weight, distance=100):
    if weight <= 0:
        return Decimal('0.00')

    base_cost = Decimal('5.00')
    weight_cost = Decimal(str(weight)) * Decimal('0.50')
    distance_multiplier = 1 + (distance / 1000)

    total_cost = (base_cost + weight_cost) * Decimal(str(distance_multiplier))
    return total_cost.quantize(Decimal('0.01'))


class InventoryManager:
    def __init__(self):
        self.operations = []

    def add_stock(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        product.stock += quantity
        product.save()

        self.operations.append({
            'type': 'add',
            'product': product.name,
            'quantity': quantity,
            'timestamp': timezone.now()
        })

    def remove_stock(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if product.stock < quantity:
            raise ValueError("Insufficient stock")

        product.stock -= quantity
        product.save()

        self.operations.append({
            'type': 'remove',
            'product': product.name,
            'quantity': quantity,
            'timestamp': timezone.now()
        })

    def get_operation_history(self):
        return self.operations.copy()