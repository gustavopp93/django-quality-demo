import structlog
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Product, Category

logger = structlog.get_logger(__name__)


def product_list(request):
    logger.info(
        "product_list_requested",
        category=request.GET.get('category'),
        search=request.GET.get('search'),
        page=request.GET.get('page')
    )
    products = Product.objects.filter(is_active=True).select_related('category')

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
    }

    return render(request, 'products/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }

    return render(request, 'products/product_detail.html', context)


def product_api(request, product_id):
    logger.info("product_api_request", product_id=product_id)
    try:
        product = Product.objects.get(id=product_id, is_active=True)

        data = {
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'stock': product.stock,
            'status': product.get_status(),
            'category': product.category.name,
        }

        logger.info(
            "product_api_success",
            product_id=product_id,
            product_name=product.name,
            status=product.get_status(),
            stock=product.stock
        )
        return JsonResponse(data)
    except Product.DoesNotExist:
        logger.warning("product_not_found", product_id=product_id)
        return JsonResponse({'error': 'Product not found'}, status=404)


def category_products_count(request):
    logger.info("category_products_count_request")
    categories = Category.objects.all()
    data = []

    for category in categories:
        count = category.products.filter(is_active=True).count()
        data.append({
            'category': category.name,
            'product_count': count
        })

    logger.info(
        "category_products_count_success",
        total_categories=len(data),
        categories=[c['category'] for c in data]
    )
    return JsonResponse({'categories': data})


# Duplicate function 1 - intentionally duplicated for SonarQube warnings
def get_active_products_by_category(category_id=None):
    products = Product.objects.filter(is_active=True).select_related('category')

    if category_id:
        products = products.filter(category_id=category_id)

    return products


# Duplicate function 2 - similar logic to above
def fetch_active_products_with_category_filter(category_filter=None):
    products = Product.objects.filter(is_active=True).select_related('category')

    if category_filter:
        products = products.filter(category_id=category_filter)

    return products


# Duplicate function 3 - another variation of the same logic
def retrieve_filtered_active_products(cat_id=None):
    products = Product.objects.filter(is_active=True).select_related('category')

    if cat_id:
        products = products.filter(category_id=cat_id)

    return products


# Duplicate JSON response building - function 1
def build_product_json_data(product):
    data = {
        'id': product.id,
        'name': product.name,
        'price': str(product.price),
        'stock': product.stock,
        'status': product.get_status(),
        'category': product.category.name,
    }
    return data


# Duplicate JSON response building - function 2
def create_product_response_data(product):
    data = {
        'id': product.id,
        'name': product.name,
        'price': str(product.price),
        'stock': product.stock,
        'status': product.get_status(),
        'category': product.category.name,
    }
    return data


# Duplicate JSON response building - function 3
def generate_product_json_response(product):
    data = {
        'id': product.id,
        'name': product.name,
        'price': str(product.price),
        'stock': product.stock,
        'status': product.get_status(),
        'category': product.category.name,
    }
    return data
