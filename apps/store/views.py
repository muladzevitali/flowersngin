from apps.store import models
from django.views.generic import ListView, DetailView
from random import sample


class StoreListView(ListView):
    template_name = 'store.html'
    queryset = models.Product.objects.all()
    paginate_by = 100
    ordering = ('id', )

    def get_queryset(self):
        return self.queryset.filter(is_published=True)


class ProductDetailView(DetailView):
    template_name = 'product-detail.html'
    model = models.Product

    def get_random_items(self, num_items):
        total_objects = self.model.objects.count()
        num_items = min(total_objects, num_items)
        object_ids = sample(range(1, total_objects + 1), num_items)
        return object_ids

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        random_product_ids = self.get_random_items(4)
        context['related_products'] = self.model.objects.filter(pk__in=random_product_ids)
        return context
