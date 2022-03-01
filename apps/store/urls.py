from django.urls import path

from apps.store import views

urlpatterns = [
    path('', views.index, name='store-index')
]
