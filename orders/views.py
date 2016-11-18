from fair.models import Fair
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied


# Create your views here.
def products(request, template_name='orders/products.html'):
    if not request.user.has_perm('orders.view_products'):
        raise PermissionDenied
    products = Product.objects.filter(fair=Fair.objects.get(name='Armada 2016'))
    return render(request, template_name, {
        'products': products,
        'total_revenue': sum([product.revenue() for product in products])
    })


# Create your views here.
def product(request, pk, template_name='orders/product.html'):
    if not request.user.has_perm('orders.view_products'):
        raise PermissionDenied
    product = get_object_or_404(Product, pk=pk)
    return render(request, template_name, {
        'product': product,
    })
