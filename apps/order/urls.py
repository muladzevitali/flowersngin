from django.urls import path

from apps.order import views

urlpatterns = [
    path('', views.place_order, name='order-index')
]
