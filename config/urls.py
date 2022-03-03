from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (path, include)

from config import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('store/', include('apps.store.urls')),
    path('cart/', include('apps.cart.urls')),
    path('order/', include('apps.order.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
