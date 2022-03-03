from django.contrib import messages
from django.shortcuts import redirect, render

from apps.cart.views import get_cart_info
from apps.order import (models, forms)


def place_order(request):
    cart_info = get_cart_info(request)
    if not cart_info['cart_items']:
        return redirect('store-index')

    form = forms.OrderForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            messages.error(request, 'Incorrect values')
            print(form.errors)
            cart_info = get_cart_info(request)
            context = dict(form=form, **cart_info)
            return render(request, 'cart-2.html', context=context)

        order = form.save(commit=False)
        order.order_total = cart_info['grand_total']
        order.tax = cart_info['tax']
        order.ip = request.META.get('REMOTE_ADDR')
        order.save()

        clear_cart(order, cart_info['cart_items'])

        context = dict(order=order)
        return render(request, 'cart-3.html', context=context)

    context = dict(form=form, **cart_info)
    return render(request, 'cart-2.html', context=context)


def clear_cart(order, cart_items):
    for cart_item in cart_items:
        order_product = models.OrderProduct(order=order, product=cart_item.product)

        order_product.quantity = cart_item.quantity
        order_product.product_price = cart_item.product.price
        order_product.is_ordered = True

        order_product.save()

        product = cart_item.product
        product.stock -= cart_item.quantity
        product.save()

    cart_items.delete()
