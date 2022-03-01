from django import forms
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.store import models


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'


class ProductAdmin(TranslationAdmin):
    form = ProductAdminForm
    prepopulated_fields = {'slug': ("name_en_us",)}
    list_display = ('pk', 'name', 'is_published', 'stock')
    list_editable = ('is_published',)


class ReviewAdmin(TranslationAdmin):
    list_display = ('pk', 'name', 'stars')
    list_editable = ('stars',)


class RecipeAdmin(TranslationAdmin):
    list_display = ('pk', 'name', 'season')


class BotanicalAdmin(TranslationAdmin):
    list_display = ('pk', 'name', 'season')



admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.Botanical, BotanicalAdmin)
