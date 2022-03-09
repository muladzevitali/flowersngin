from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (path, include, )

from config import views

urlpatterns = [
    path(r'i18n/', include('django.conf.urls.i18n')),
    path('', views.index, name='index'),
    path('store/', include('apps.store.urls')),
    path('cart/', include('apps.cart.urls')),
    path('order/', include('apps.order.urls')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('fadmin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
