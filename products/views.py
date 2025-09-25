from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Product, Category


def product_list(request):
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

        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


def category_products_count(request):
    categories = Category.objects.all()
    data = []

    for category in categories:
        count = category.products.filter(is_active=True).count()
        data.append({
            'category': category.name,
            'product_count': count
        })

    return JsonResponse({'categories': data})
