from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.order import models


class CountryAdmin(TranslationAdmin):
    list_display = ('pk', 'name',)


class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


class PaymentInline(admin.StackedInline):
    model = models.Payment
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'client_full_name', 'client_email', 'order_total', 'tax', 'status', 'ip')
    list_filter = ('status', 'is_ordered',)
    search_fields = ('order_number', 'client_first_name', 'client_last_name', 'client_email', 'receiver_first_name',
                     'receiver_last_name',)
    list_per_page = 50
    inlines = (OrderProductInline, PaymentInline,)


admin.site.register(models.Country, CountryAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderProduct)
