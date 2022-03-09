from modeltranslation.translator import register, TranslationOptions

from apps.store import models


@register(models.Season)
class SeasonTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(models.Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(models.Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(models.Recipe)
class RecipeTranslationOptions(TranslationOptions):
    fields = ('name', 'text',)


@register(models.Botanical)
class BotanicalTranslationOptions(TranslationOptions):
    fields = ('name', )