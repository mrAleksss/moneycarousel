from django.shortcuts import get_object_or_404, render
from .models import Category, Product


def product_all(request):
    products = Product.products.all()
    return render(request, 'store/home.html', {'products': products})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    # session stuf
    # recently_viewed_products = None
    
    # if 'recently_viewed' in request.session:
    #     if product.id in request.session['recently_viewed']:
    #         request.session['recently_viewed'].remove(product.id)
         
    #     recently_viewed_products = Product.objects.filter(pk__in=request.session['resently_viewed'])    
    #     request.session['recently_viewed'].insert(0, product.id)
    #     if len(request.session['recently_viewed']) > 5:
    #             request.session['recently_viewed'].pop()
            
    # else:
    #     request.session['recently_viewed']=[product.id]
    # request.session.modified = True
    
    return render(request, 'store/products/single.html', {'product': product})
