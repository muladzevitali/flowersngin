from django.contrib import messages
from django.shortcuts import (redirect, render, reverse, get_object_or_404)

from apps.cart.views import get_cart_info
from apps.order import (utils, forms, helpers, models)


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
        with helpers.MollieClient() as client:
            payment_meta = client.create_payment(request, order)

        _ = models.Payment.from_meta(payment_meta, order)

        return redirect(payment_meta.checkout_url)

    context = dict(form=form, **cart_info)
    return render(request, 'cart-2.html', context=context)


def post_payment(request, order_number):
    order = get_object_or_404(models.Order, order_number=order_number)
    payment = order.order_payments.first()
    with helpers.MollieClient() as client:
        status = client.get_payment_status(payment.payment_id)

    if not status == 'paid':
        return redirect(reverse('order-index'))

    cart_info = get_cart_info(request)
    utils.finalize_order(order, payment, cart_info['cart_items'])
    utils.notify_on_completion(request, order, cart_info)
    cart_info['cart_items'].delete()

    context = dict(order=order)
    return render(request, 'cart-3.html', context=context)
