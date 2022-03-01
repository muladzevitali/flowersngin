from django.urls import path

from apps.cart import views

urlpatterns = [
    path('', views.index, name='cart-index')
]
