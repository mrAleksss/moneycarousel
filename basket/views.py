from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from djmoney.contrib.exchange.models import get_rate

from store.models import Product

from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    rate = get_rate('USD', "UAH")
    return render(request, 'basket/summary.html', {'basket': basket, 'rate': rate})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        basketuah = basket.basket_uah_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal, 'basketuah':basketuah})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        basketsubtotal = basket.get_subtotal_price()
        basketuah = basket.basket_uah_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': basketsubtotal, 'basketuah':basketuah})
        return response


