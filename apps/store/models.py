from ckeditor.fields import RichTextField
from django.core.validators import (MinValueValidator, MaxValueValidator)
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


def get_cart_id(request):
    return request.session.session_key or request.session.create()


class Season(TimeStampedModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Product(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True, verbose_name=_('name'))
    slug = models.SlugField(max_length=200, unique=True)
    description = RichTextField(max_length=500, blank=True, verbose_name=_('description'))
    price = models.FloatField(verbose_name=_('price'))
    images = models.ImageField(upload_to='photos/products', null=True, blank=True)
    stock = models.IntegerField(verbose_name=_('stock'))
    is_published = models.BooleanField(default=True, verbose_name=_('published'))

    def __str__(self):
        return self.name

    @property
    def url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    @property
    def add_to_cart_url(self):
        return reverse('add_to_cart', args=[self.id])

    @property
    def remove_from_cart_url(self):
        return reverse('remove_from_cart', args=[self.id])

    @property
    def remove_cart_item_url(self):
        return reverse('remove_cart_item', args=[self.id])


class Review(TimeStampedModel):
    text = RichTextField()
    name = models.CharField(max_length=100)
    stars = models.IntegerField(validators=(MinValueValidator(0), MaxValueValidator(5)), default=0)

    def __str__(self):
        return f'Review({self.id})-{self.name}'


class Recipe(TimeStampedModel):
    name = models.CharField(max_length=100)
    text = RichTextField()
    season = models.ForeignKey(to='store.Season', on_delete=models.CASCADE, related_name='season_related_recipes')
    image = models.ImageField(upload_to='photos/recipes')

    def __str__(self):
        return f'Recipe({self.id}) - {self.name}'


class Botanical(TimeStampedModel):
    name = models.CharField(max_length=100)
    season = models.ForeignKey(to='store.Season', on_delete=models.CASCADE, related_name='season_related_botanicals')
    image = models.ImageField(upload_to='photos/botanicals')

    def __str__(self):
        return f'Botanical({self.id}) - {self.name}'
