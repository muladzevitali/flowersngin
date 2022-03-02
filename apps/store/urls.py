from django.urls import path

from apps.store import views

urlpatterns = [
    path('', views.StoreListView.as_view(), name='store-index'),
    path('<pk>', views.ProductDetailView.as_view(), name='product-detail'),
]
