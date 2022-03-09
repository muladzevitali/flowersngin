from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel


def get_cart_id(request):
    return request.session.session_key or request.session.create()


# Create your models here.
class Cart(TimeStampedModel):
    cart_id = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f'Cart({self.id}) - {self.cart_id}'


class CartItem(TimeStampedModel):
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, related_name='product_cart_items')
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')

    def __str__(self):
        return f'CartItem({self.id}) - {self.product.name}'

    @property
    def total(self):
        return self.product.price * self.quantity

    @property
    def increment_cart_item_quantity_url(self):
        return reverse('increment_cart_item_quantity', args=[self.id])

    @property
    def decrement_cart_item_quantity_url(self):
        return reverse('decrement_cart_item_quantity', args=[self.id])

    @property
    def remove_cart_item_url(self):
        return reverse('remove_cart_item', args=[self.id])
