from django.urls import path

from apps.cart import views

urlpatterns = [
    path('', views.index, name='cart-index'),
    path('add/<product_id>', views.add_to_cart, name='add-to-cart'),
    path('remove-item/<int:cart_item_id>', views.remove_cart_item, name='remove_cart_item'),
    path('increment-item-quantity/<int:cart_item_id>', views.increment_cart_item_quantity,
         name='increment_cart_item_quantity'),
    path('decrement-item-quantity/<int:cart_item_id>', views.decrement_cart_item_quantity,
         name='decrement_cart_item_quantity'),
]
