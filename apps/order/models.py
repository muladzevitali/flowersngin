from datetime import datetime

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel


class Country(TimeStampedModel):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __str__(self):
        return self.name


class Payment(TimeStampedModel):
    class PaymentStatusChoices(models.TextChoices):
        OPEN = _('open')
        FAILED = _('failed')
        PENDING = _('pending')
        PAID = _('paid')

    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100, default='mollie')
    description = models.CharField(max_length=255, null=True, blank=True)
    checkout_url = models.URLField(null=True, blank=True)
    amount_paid = models.CharField(max_length=20)
    ccy = models.CharField(max_length=10)
    status = models.CharField(max_length=100, choices=PaymentStatusChoices.choices)
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='order_payments')

    @classmethod
    def from_meta(cls, meta, order):
        payment = cls()
        payment.payment_id = meta.id
        payment.description = meta.description
        payment.checkout_url = meta.checkout_url
        payment.status = meta.status
        payment.amount = meta.amount["value"]
        payment.ccy = meta.amount['currency']
        payment.order = order
        payment.save()
        return payment

    def __str__(self):
        return f'{self.payment_id}'


class Order(TimeStampedModel):
    class OrderStatusChoices(models.TextChoices):
        NEW = _('new')
        ACCEPTED = _('accepted')
        COMPLETED = _('completed')
        CANCELED = _('canceled')

    order_number = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    btw_number = models.CharField(max_length=100, null=True, blank=True)
    client_first_name = models.CharField(max_length=50)
    client_last_name = models.CharField(max_length=50)
    client_phone = models.CharField(max_length=15)
    client_email = models.EmailField()
    client_street_name = models.CharField(max_length=400)
    client_house_number = models.CharField(max_length=100)
    client_bus = models.CharField(max_length=10)
    client_city = models.CharField(max_length=100)
    client_postalcode = models.CharField(max_length=20)
    client_country = models.ForeignKey('order.Country', on_delete=models.CASCADE, related_name='country_client_orders')
    pick_up_from_store = models.BooleanField(default=False)
    different_deliver_address = models.BooleanField(default=False)
    receiver_first_name = models.CharField(max_length=50, null=True, blank=True)
    receiver_last_name = models.CharField(max_length=50, null=True, blank=True)
    receiver_street_name = models.CharField(max_length=400, null=True, blank=True)
    receiver_house_number = models.CharField(max_length=100, null=True, blank=True)
    receiver_bus = models.CharField(max_length=10, null=True, blank=True)
    receiver_city = models.CharField(max_length=100, null=True, blank=True)
    receiver_postalcode = models.CharField(max_length=20, null=True, blank=True)
    receiver_country = models.ForeignKey('order.Country', on_delete=models.CASCADE, null=True, blank=True,
                                         related_name='country_receiver_orders')

    order_note = models.TextField(null=True, blank=True)
    order_total = models.DecimalField(max_digits=8, decimal_places=2)
    tax = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=OrderStatusChoices.choices, default=OrderStatusChoices.NEW)
    ip = models.CharField(max_length=20, blank=True)
    is_ordered = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    @property
    def client_full_name(self):
        return f'{self.client_first_name} {self.client_last_name}'

    @property
    def receiver_full_name(self):
        return f'{self.receiver_first_name} {self.receiver_last_name}'

    @property
    def client_full_address(self):
        address = f'{self.client_street_name} {self.client_house_number}'
        if self.client_bus:
            address += f' / {self.client_bus}'
        address += f', {self.client_country.name}, {self.client_postalcode}'
        return address

    @property
    def receiver_full_address(self):
        address = f'{self.receiver_street_name} {self.receiver_house_number}'
        if self.receiver_bus:
            address += f' / {self.receiver_bus}'
        address += f', {self.receiver_country.name}, {self.receiver_postalcode}'
        return address

    @property
    def order_address(self):
        if self.pick_up_from_store:
            return _('Pick up from store')
        elif self.different_deliver_address:
            return self.receiver_full_address
        else:
            return self.client_full_address

    def __str__(self):
        return f'Order({self.id}) - {self.order_number}'

    @staticmethod
    def create_order_id(sender, instance: 'Order', **kwargs):
        if instance.order_number:
            return

        current_date = datetime.now().strftime('%Y%m%d')
        instance.order_number = f'ORD{current_date}{instance.id}'
        instance.save()


class OrderProduct(models.Model):
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, related_name='product_orders')
    quantity = models.SmallIntegerField()
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_ordered = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Order product')
        verbose_name_plural = _('Order products')

    @property
    def total(self):
        return self.quantity * self.product_price

    def __str__(self):
        return f'{self.order} - {self.product}'


post_save.connect(Order.create_order_id, sender=Order)
