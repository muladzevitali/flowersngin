from django.shortcuts import (render, get_object_or_404, redirect)
from apps.store.models import Product
from apps.cart.models import (Cart, CartItem, get_cart_id)
from django.views.decorators.http import require_http_methods
from . import forms
from django.conf import settings


def get_cart_info(request):
    cart, _ = Cart.objects.get_or_create(cart_id=get_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)

    total = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    quantity = sum(cart_item.quantity for cart_item in cart_items)
    tax = settings.TAX * total
    grand_total = total + tax

    context = dict(cart_items=cart_items, total=total, quantity=quantity, tax=tax, grand_total=grand_total)

    return context


# Create your views here.
def index(request):
    cart_id = get_cart_id(request)
    cart, _ = Cart.objects.get_or_create(cart_id=cart_id)
    context = get_cart_info(request)

    return render(request, 'cart-1.html', context=context)


@require_http_methods(request_method_list=['POST'])
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, stock__gt=0)
    form = forms.AddToCartForm(request.POST)
    if not form.is_valid():
        return redirect(product.url)

    cart_id = get_cart_id(request)
    cart, _ = Cart.objects.get_or_create(cart_id=cart_id)

    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart,
                                                        defaults={'quantity': form.cleaned_data['quantity']})
    if not created:
        cart_item.quantity += form.cleaned_data['quantity']
        cart_item.save()

    return redirect('cart-index')


def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    cart_item.delete()

    return redirect('cart')


def increment_cart_item_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart-index')


def decrement_cart_item_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart-index')
